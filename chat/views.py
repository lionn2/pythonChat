from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
import json
import datetime
from django.core import serializers
import dateutil.parser
import time
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as inlog, logout as outlog
from models import Chat, Message, query_to_json, Document
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from itertools import chain

from django.template import RequestContext
from django.core.urlresolvers import reverse
from forms import DocumentForm

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


def user_chats(request):
	if (request.user.is_authenticated()):
		chats = Chat.objects.all()
		user_chat = []
		is_user = False
		for ch in chats:
			users = ch.users.all()
			for us in users:
				if str(us) == str(request.user):
					if user_chat == []:
						user_chat.append(ch)
					else:
						user_chat.append(ch)
					break
		return render(request, 'index.html', {'chats': user_chat } )
	else:
		return redirect('/')

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
				return HttpResponse("disable account")
		else:
			print "invalid account"
			return redirect('/', status = 401)
	except:
		return HttpResponse('bad')
		#return HttpResponseForbidden()
		#return redirect('/', status = 400)


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
			"form": DocumentForm(),
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
	if request.user.is_authenticated():
		chat_name = request.POST['chat_name']
		chat = Chat(
			chat_name = chat_name,
			start_time = timezone.now(),
			owner = str(request.user),
			)
		chat.save()
		return redirect('chat', id=chat.id)
	else:
		return redirect('/', status = 403)
	
	

def delete_chat(request):
	if request.user.is_authenticated():
		chat_id = request.POST['id']
		try:
			chat = Chat.objects.get(id = chat_id)
			if str(request.user) == chat.owner:
				messages = Message.objects.filter(chat_id = chat)
				messages.delete()
				chat.delete()
				return HttpResponse('ok')
			else:
				return HttpResponse("Error", status = 403)
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


def add_file(request, chat_id):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				chat = Chat.objects.get(id = chat_id)
				newdoc = Document(docfile = request.FILES['docfile'])
				newdoc.save()
				text = newdoc.docfile
				message = Message(
					chat_id = chat,
					user_id = request.user,
					message = text,
					post_time = timezone.now(),
					_type = 3,
					)
				message.save()
				return HttpResponse(request.FILES['docfile'].name)
			except:
				return HttpResponse('bad')
	else:
		form = DocumentForm()
		return render(request, 'add_file.html', {'form': form } )


def search(request):
	text = request.POST['text']
	_type = request.POST['_type']
	if _type == 0:
		messages = Message.objects.filter(message__contains = str(text))
		return render(request, 'search.html', {'result': messages })
	elif _type == 1:
		chats = Chat.objects.filter(chat_name__contains = str(text))
		return render(request, 'search.html', {'result': chats })
	elif _type == 2:
		users = User.objects.filter(username__contains = str(text))
		return render(request, 'search.html', {'result': users })
	else:
		return redirect('/')