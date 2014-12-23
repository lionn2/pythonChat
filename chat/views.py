from django.shortcuts import render, redirect, render_to_response
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
from models import Chat, Message, query_to_json, UploadFileForm
from django.core.urlresolvers import reverse

def index(request):
	result = {
		"chats": Chat.objects.all()
	}
	return render(request, 'index.html', result)

def registration(request):
	return render(request, 'registration.html')

def check_username(request):
	try:
		username = request.POST['username']
		user = User.objects.get(username = username)
		return HttpResponse('error', status=400)
	except:
		return HttpResponse('ok')

def create_user(request):
	try:	
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
	except:
		return HttpResponse(status=401)

def login(request):
	try:
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
			return redirect('/', status = 401)
	except:
		return redirect('/', status = 400)


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
			return HttpResponse("Error", status = 400)
	else:
		return HttpResponse("Error", status  = 400)

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
						message = str(request.user) + " entered to chat",
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
	if request.user.is_authenticated():
		chat_id = request.POST['id']
		try:
			chat = Chat.objects.get(id = chat_id)
			messages = Message.objects.filter(chat_id = chat)
			messages.delete()
			chat.delete()
			return HttpResponse('ok')
		except:
			return render('/')
	else:
		return HttpResponse("Error", status = 401)

def delete_user_from_chat(request):
	username = request.user
	chat_id = request.POST['chat_id']
	try:
		chat = Chat.objects.get(id=chat_id)
		chat.users.remove(username)
		mess = Message( 
			chat_id = chat,
			user_id = request.user,
			message = str(request.user) + " left from chat",
			post_time = timezone.now(),
			_type = 2,
		)
		mess.save()
		return HttpResponse(json.dumps(mess.to_json()))
	except Exception, e:
		return HttpResponse("Error", status = 400)

def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			return HttpResponse('ok')
	else:
		form = UploadFileForm()
	return HttpResponse(status = 404)

def handle_uploaded_file(f):
	with open('buffer.txt', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)