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
from models import Chat, Message

def index(request):
	result = {
		"chats": Chat.objects.all()
	}
	return render(request, 'index.html', result)

def name(request):
	return render(request, 'name.html')

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
	print '111111111111111111111'
	#time.sleep(5)
	outlog(request)
	print '222222222222222222222'
	return redirect('/')


def drop_user(request, id):
	user = User.objects.get(id=id)
	user.delete()
	return HttpResponse('result:ok')


def post_message(request, chat_id):
	if request.user.is_authenticated():
		message = request.POST['message']
		user_id = request.POST['user_id']
		post_time = timezone.now()
		post_time += timedelta(hours = 2)
		chat = Chat.objects.get(id = chat_id)
		user = User.objects.get(id = user_id)
		m = Message(user_id = user, 
			chat_id = chat,
			message = message,
			post_time = post_time
			)
		m.save()
		return HttpResponse(serializers.serialize("json", [m,]))
	else:
		return HttpResponse("fail")


def edit_message(request, user_id, id):
	message = Message.objects.get(id = id)
	if message.user_id.id == user_id:
		return HttpResponse(json.dumps(message.to_json()))
	else:
		return HttpResponse('result:no')


def post_edit_message(request, user_id, id):
	message = Message.objects.get(id=id)
	if user_id == message.user_id.id:
		message.message = request.POST['message']
		message.post_time = datetime.datetime.now()
		return HttpResponse(json.dumps(message.to_json()))
	else:
		return HttpResponse('result:no')


def delete_message(request, user_id, id):
	message = Message.objects.get(id = id)
	if message.user_id.id == user_id:
		message.delete()
		return HttpResponse('result:ok')
	else:
		return HttpResponse('result:no')


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
				users = []
				for i in range(len(messages)):
					users.append(messages[i].user_id.name)
				print users
				mes = {
					'messages': serializers.serialize("json", messages),	#my messages
					'users': json.dumps(users),			#my users
				}
				return HttpResponse(mes)
			time.sleep(1)
	else:
		return HttpResponse(serializers.serialize("json", messages))
	return HttpResponse("[]")