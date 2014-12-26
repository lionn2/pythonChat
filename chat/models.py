from django.db import models
from django.contrib.auth.models import User
import json

class Chat(models.Model):
	chat_name = models.CharField(max_length = 100)
	start_time = models.DateTimeField()
	users = models.ManyToManyField(User)
	guest = models.IntegerField(default=0)

	def to_json(self):
		return {
			"id": self.id,
			"chat_name": self.chat_name,
			"start_time": str(self.start_time),
		}


class Message(models.Model):
	chat_id = models.ForeignKey(Chat)
	user_id = models.ForeignKey(User)
	message = models.TextField()
	post_time = models.DateTimeField()
	_type = models.IntegerField(default=0)

	def to_json(self):
		return {
			"id": self.id,
			"chat_id": self.chat_id.id,
			"user": self.user_id.username,
			"message": self.message,
			"post_time": str(self.post_time),
			"type": self._type,
		}

def query_to_json(data):
	mess = []
	for m in data:
		mess.append(m.to_json())
 	return json.dumps(mess)


class Document(models.Model):
	docfile = models.FileField(upload_to='documents/%Y/%m/%d')
