from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Password

from pusherable.mixins import PusherDetailMixin
# Create your views here.
def index(request):
	passwords = Password.objects.order_by('-name')
	context = {
		'passwords': passwords
	}
	return render(request,'pwmanager/index.html',context)

def create(request):
	return HttpResponse('Hello!')
