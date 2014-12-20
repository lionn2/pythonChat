from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
	chat_name = models.CharField(max_length = 100)
	start_time = models.DateTimeField()
	users = models.ManyToManyField(User)

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

	def to_json(self):
		return {
			"id": self.id,
			"chat_id": self.chat_id.id,
			"user": self.user_id.name,
			"message": self.message,
			"post_time": str(self.post_time),
		}