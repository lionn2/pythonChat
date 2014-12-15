from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import json
import datetime

from models import Chat, Message, User

def index(request):
	return render(request, 'index.html')

def name(request):
	return render(request, 'name.html')

def create_user(request):
	name = request.POST['name']
	date_registration = datetime.datetime.now()
	user = User(name = name, date_registration = date_registration)
	user.save()
	return HttpResponse('result:ok')


def post_message(request, chat_id):
	message = request.POST['message']
	post_time = DateTime.today()
	chat = Chat.objects.get(id = chat_id)
	m = Message(user_id = user, 
		chat_id = chat,
		message = message,
		post_time = post_time
		)
	m.save()
	return HttpResponse('result:ok')

def all_messages_by_chat(request, chat_id):
	messages = Message.objects.filter(chat_id = chat_id).all()
	r = messages.__dict__
	result = json.dumps(r)
	return messages


def all_chats(request):
	chats = Chat.objects.all()
	data = []
	for chat in chats:
		data.append(chat.to_json())
	return json.dumps(data)