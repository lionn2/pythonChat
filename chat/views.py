from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import json

from models import Chat, Message, User

def index(request):
	return render(request, 'index.html')


def create_user(request):
	name = request.POST['name']
	date_registration = DateTime.today()
	user = User(name = name, date_registration = date_registration)
	user.save()
	return HttpResponse('result:ok')


def post_message(request, user_id, chat_id):
	message = request.POST['message']
	post_time = DateTime.today()
	user = User.objects.get(id = user_id)
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
	result = json.dumps(messages)
	return messages