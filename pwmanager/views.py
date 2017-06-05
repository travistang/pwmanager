from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.template import loader
from .models import Password
from .templatetags.password_filters import json_friendly
from urllib.parse import parse_qs
from pusherable.mixins import PusherDetailMixin
from django.forms.models import model_to_dict
from channels import Group
import json
# helper functions
def get_all_passwords():
	res = []
	for p in Password.objects.all().order_by('-date_created'):
		res.append(model_to_dict(p))
	return res
def send_password(obj):
	Group('users').send({'text':json.dumps(json_friendly(obj))})
# Create your views here.
def index(request):
	passwords = Password.objects.order_by('-name')
	context = {
		'passwords': passwords
	}
	return render(request,'pwmanager/index.html',context)

def create(request):
	print(request)
	req_dict = parse_qs(request.body)
	response = {}
	# TODO: how about csrf token?
	if b'pw-proposed' not in req_dict or b'pw-name' not in req_dict:
		response['status'] = 'fail'
	else:
		pw = req_dict[b'pw-proposed'][0].decode('utf-8')
		name = req_dict[b'pw-name'][0].decode('utf-8')
		# create object and store the data
		pw_entry = Password(name = name,password = pw)
		pw_entry.save()
		if len(pw) == 0 or len(name) == 0:
			response['status'] = 'fail'
		else:
			response['status'] = 'ok'
		# how about the channel...?
		send_password(model_to_dict(pw_entry))
	return JsonResponse(response)
