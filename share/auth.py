from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from cts.share.forms import *
from cts.share.views import r2r

def login(request):
	if not request.user.is_authenticated():
		form = LoginForm(request.POST or None)
		if form.is_valid():
			userName = form.cleaned_data['username']
			passWord = form.cleaned_data['password']
			#print passWord
			user = auth.authenticate(username=userName, password=passWord)
			if user is not None:
				auth.login(request, user)
				return HttpResponseRedirect('/tweetboard/')
			return HttpResponse('fail')
		return r2r(request, 'login.html', {'form': form})
	return HttpResponseRedirect('/')

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

import util
def register(request):
	if not request.user.is_authenticated():
		form = RegisterForm(request.POST or None)
		if form.is_valid():
			userName = form.cleaned_data['username']
			passWord = form.cleaned_data['password']
			eMail = form.cleaned_data['email']
			firstName = form.cleaned_data['first_name']
			lastName = form.cleaned_data['last_name']
			user = User.objects.create_user(
                        username=userName,
                        email=eMail,
                        password=passWord,
                        )
			url = util.gen_url()
			UserProfile.objects.create(user=user, url=url)
			return HttpResponseRedirect('/')
		return r2r(request, 'register.html', {'form': form})
	return HttpResponseRedirect('/')

