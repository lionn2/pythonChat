from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import json
import datetime
from django.core import serializers

from models import Chat, Message, User

def index(request):
	result = {
		"chats": Chat.objects.all()
	}
	return render(request, 'index.html', result)

def name(request):
	return render(request, 'name.html')

def create_user(request, chat_id):
	name = request.POST['name']
	date_registration = datetime.datetime.now()
	user = User(name = name, date_registration = date_registration)
	user.save()
	chat = Chat.objects.get(id=chat_id)
	chat.users.add(user)
	chat.save()
	user_to_json = json.dumps(user.to_json())
	return HttpResponse(user_to_json)


def drop_user(self, id):
	user = User.objects.get(id=id)
	user.delete()
	return HttpResponse('result:ok')


def post_message(request, chat_id):
	message = request.POST['message']
	user_id = request.POST['user_id']
	post_time = datetime.datetime.now()
	chat = Chat.objects.get(id = chat_id)
	user = User.objects.get(id = user_id)
	m = Message(user_id = user, 
		chat_id = chat,
		message = message,
		post_time = post_time
		)
	m.save()
	return HttpResponse(json.dumps(m.to_json()))


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
	chat = {
		"chat": Chat.objects.get(id=id),
		"messages": Message.objects.filter(chat_id = id).all(),
	}
	return render(request, 'chat.html', chat)

def messages_from_date(request, chat_id):
	date = request.POST['date']
	d = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
	messages = Message.objects.filter(chat_id = chat_id).filter(post_time__gte = d)	
	data = serializers.serialize("json", messages)
	return HttpResponse(data)