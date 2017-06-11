from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from .models import Password, PendingDeviceRequest
from .templatetags.password_filters import json_friendly
from urllib.parse import parse_qs
from pusherable.mixins import PusherDetailMixin
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from django.contrib.auth import authenticate as auth, login as loi
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from channels import Group
import json
import re
# helper functions
def get_all_passwords():
	res = []
	for p in Password.objects.all().order_by('-date_created'):
		res.append(model_to_dict(p))
	return res
def send_password(obj):
	Group('users').send({'text':json.dumps(json_friendly(obj))})

def send_delete_notice(obj):
	print('sending notice:',json.dumps(obj))
	Group('users').send({'text':json.dumps(obj)})

@login_required
def request_code(request):
	# TODO: will something go wrong here?
	pdr = PendingDeviceRequest()
	pdr.save()
	print(pdr.code)
	return JsonResponse({'code':pdr.code})

def send_modify_notice(obj):
	print ('sending modification notice',json.dumps(obj))
	Group('users').send({'text':json.dumps(obj)})
# Create your views here.
@login_required
def index(request):
	passwords = Password.objects.order_by('-name')
	context = {
		'passwords': passwords
	}
	return render(request,'pwmanager/index.html',context)

# TODO: this
@login_required
def authorize(request,code = None):
	if not PendingDeviceRequest.objects.filter(code = code).exists():
		pass
	pass

@login_required
def remove(request):
	request = request.body.decode('utf-8')
	req_dict = json.loads(request)
	response = {}
	if 'name' not in req_dict:
		response['status'] = 'fail'
	else:
		name = req_dict['name']
		pw_entry = Password.objects.get(name = name)
		if not pw_entry:
			response['status'] = 'fail'
		else:
			pw_entry.delete()
			response['status'] = 'ok'
			send_delete_notice({'action': 'deleted','name':name})
	return JsonResponse(response)

@login_required
def create(request):
	print(request)
	req_dict = parse_qs(request.body)
	response = {}
	if b'pw-proposed' not in req_dict or b'pw-name' not in req_dict:
		response['status'] = 'fail'
	else:
		pw = req_dict[b'pw-proposed'][0].decode('utf-8')
		name = req_dict[b'pw-name'][0].decode('utf-8')
		if not Password.objects.filter(name = name).exists():
			# create object and store the data
			if len(pw) == 0 or len(name) == 0:
				response['status'] = 'fail'
			else:
				response['status'] = 'ok'
				pw_entry = Password(name = name,password = pw)
				pw_entry.save()
				send_password(model_to_dict(pw_entry))
		else:
			# modify existing object and store the data

			if len(pw) == 0:
				response['status'] = 'fail'
			else:
				response['status'] = 'ok'
				cur_pw = Password.objects.get(name = name)
				cur_pw.password = pw
				cur_pw.save()
				send_modify_notice({'action': 'modified','updated_pw':json_friendly(model_to_dict(cur_pw))})
	return JsonResponse(response)

def register(request):
	if request.method == 'GET':
		return JsonResponse({'result':'fail','reason':'GET request is not accepted for this URL'})
	
	if User.objects.filter(is_staff = False).count() > 0:
		return JsonResponse({'result': 'fail','reason':'An account has already been registered. Did you forget your password?'})
	
	req_form = parse_qs(request.body.decode('utf-8'))
	# checking the form on server side
	# checking the form integrity
	for attr in ['username','email','register-submit','confirm-password','csrfmiddlewaretoken','password']:
		if attr not in req_form:
			return JsonResponse({'result':'fail','reason':'One of the form columns are missing'})
	# validating the form data
	username = req_form['username'][0]
	email = req_form['email'][0]
	password = req_form['password'][0]
	c_password = req_form['confirm-password'][0]
	if not re.match(r'^[^@|\s]+@[^@]+\.[^@|\s]+$',email):
		return JsonResponse({'result':'fail','reason':'Invalid email address'})

	if password != c_password:
		return JsonResponse({'result':'fail','reason':'Password and confirm password do not match'})
	
	# add user
	User.objects.create_user(username,email,password)
	return JsonResponse({'result':'success'})

def authenticate(request):
	if request.user.is_authenticated():
		return redirect('index')
	else:
		username = request.POST['username']
		password = request.POST['password']
		user = auth(request, username=username, password=password)
		if user is not None:
			loi(request,user)
			return redirect('index')
		else:
			return JsonResponse({'status': 'fail'})

# present login page to the user if he is not logged in
# otherwise redirect him to index.html
def login(request):
	print(request.user)
	if request.user.is_authenticated():
		return redirect('index')
	# render the login page
	else:
		return render(request,'pwmanager/login.html')
