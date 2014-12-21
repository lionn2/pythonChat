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
from models import Chat, Message, query_to_json#, UploadForm, Upload
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
	if Chat.objects.filter(id = chat_id) is not None:
		if request.user.is_authenticated():
			message = request.POST['message']
			user = request.user
			post_time = timezone.now()
			chat = Chat.objects.get(id = chat_id)
			m = Message(user_id = user, 
				chat_id = chat,
				message = message,
				post_time = post_time,
				_type = 0
				)
			print message
			
			m.save()
			print message
			
			return HttpResponse(json.dumps(m.to_json()))
		else:
			return HttpResponse("Error", status_code = 400)
	else:
		return HttpResponse("Error", status_code = 400)

def chat(request, id):
	try:
		chat = None
		try:
			if request.user.is_authenticated():
				chat = Chat.objects.get(id=id)
				_is = True
				if chat.users.count() is not 0:
					for u in chat.users.all():
						if u == request.user:
							_is = False	
							break
				if _is:
					chat.users.add(request.user)
					message = Message(
						chat_id = chat,
						user_id = User.objects.get(username = request.user),
						message = str(request.user) + " enter to chat",
						post_time = timezone.now(),
						_type = 1,
						)
					message.save()
					chat.save()
			else:
				chat = Chat.objects.get(id=id)
				chat.guest += 1
				chat.save()
		except:
			return redirect('/')
		users = chat.users.all()
		
		_chat = {
			"chat": Chat.objects.get(id=id),
			"messages": Message.objects.filter(chat_id = id),
		}
		chat = Chat.objects.get(id = id)
		return render(request, 'chat.html', _chat)	
	except Exception, e:
		print e
		return redirect('/')


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
		return HttpResponse('ok')
	except:
		return render('/')


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