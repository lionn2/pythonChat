from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
import json
import datetime
from django.core import serializers
import dateutil.parser
import time
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as inlog, logout as outlog
from models import Chat, Message, query_to_json, UploadForm, Upload
from django.core.urlresolvers import reverse

def index(request):
	result = {
		"chats": Chat.objects.all()
	}
	return render(request, 'index.html', result)

def registration(request):
	return render(request, 'registration.html')

def create_user(request):
	username = request.POST['username']
	password = request.POST['password']
	user = User.objects.create_user(
		username = username,
		email = request.POST['email'],
		password = password,
		first_name = request.POST['first_name'],
		last_name = request.POST['last_name'],
		)

	user.save()

	user = authenticate(username = username, password = password)
	
	print user

	if user is not None:
		if user.is_active:
			inlog(request, user)
			return redirect('/')
		else:
			print "disable account"
			return HttpResponse("disable account")
	else:
		print "invalid account"
		return HttpResponse("invalid account")


def login(request):
	user = authenticate(username = request.POST['username'], password = request.POST['password'])
	if user is not None:
		if user.is_active:
			inlog(request, user)
			return redirect('/')
		else:
			print "disable account"
			return HttpResponse("disable account")
	else:
		print "invalid account"
		return HttpResponse("invalid account")

def logout(request):
	outlog(request)
	return redirect('/')


def post_message(request, chat_id):
	if request.user.is_authenticated():
		message = request.POST['message']
		user = request.user
		post_time = timezone.now()
		chat = Chat.objects.get(id = chat_id)
		m = Message(user_id = user, 
			chat_id = chat,
			message = message,
			post_time = post_time
			)
		print message
		
		m.save()
		print message
		
		return HttpResponse(json.dumps(m.to_json()))
	else:
		return HttpResponse("fail")


def chat(request, id):
	try:
		chat = {
			"chat": Chat.objects.get(id=id),
			"messages": Message.objects.filter(chat_id = id).all(),
		}

		return render(request, 'chat.html', chat)	
	except Exception, e:
		return HttpResponse("No chats")
	

def messages_from_id(request, chat_id):
	id = request.POST['id']
	messages = Message.objects.filter(chat_id = chat_id).filter(id__gt = id)
	if len(messages) == 0:
		for i in range(30):
			messages = Message.objects.filter(chat_id = chat_id).filter(id__gt = id)
			if len(messages) > 0:
				return HttpResponse(query_to_json(messages))
			time.sleep(1)
	else:
		return HttpResponse(query_to_json(messages))
	return HttpResponse("[]")

def create_chat(request):
	chat_name = request.POST['chat_name']
	chat = Chat(
		chat_name = chat_name,
		start_time = timezone.now()
		)
	chat.save()
	return redirect('chat', id=chat.id)
	

def delete_chat(request):
	chat_id = request.POST['id']
	try:
		chat = Chat.objects.get(id = chat_id)
		messages = Message.objects.filter(chat_id = chat)
		messages.delete()
		chat.delete()
		return render('/')
	except:
		return HttpResponse('fail')


def upload(request):
    if request.method=="POST":
        img = UploadForm(request.POST, request.FILES)       
        if img.is_valid():
            img.save()  
            return HttpResponseRedirect(reverse('upload'))
    else:
        img=UploadForm()
    images=Upload.objects.all()
    return render(request,'chat.html',{'form':img,'images':images})