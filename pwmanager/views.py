from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.template import loader
from .models import Password
from urllib.parse import parse_qs
from pusherable.mixins import PusherDetailMixin
# Create your views here.
def index(request):
	passwords = Password.objects.order_by('-name')
	context = {
		'passwords': passwords
	}
	return render(request,'pwmanager/index.html',context)

def create(request):
	req_dict = parse_qs(request.body)
	response = {}
	# TODO: how about csrf token?
	if b'pw-proposed' not in req_dict or b'pw-name' not in req_dict:
		response['status'] = 'fail'
	else:
		pw = req_dict[b'pw-proposed'][0].decode('utf-8')
		name = req_dict[b'pw-name'][0].decode('utf-8')
		print(pw)
		print(name)
		if len(pw) == 0 or len(name) == 0:
			response['status'] = 'fail'
		else:
			response['status'] = 'ok'
	return JsonResponse(response)
