from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import json
import datetime

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


#def create_chat(self):



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

def chat(request, id):
	chat = {
		"chat": Chat.objects.get(id=id)
		"messages": Message.objects.filter(chat_id = id).all()
	}
	return render(request, 'chat.html', chat)

