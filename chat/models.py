from django.db import models

class User(models.Model):
	name = models.CharField(max_length=100)
	date_registration = models.DateTimeField()

class Chat(models.Model):
	chat_name = models.CharField(max_length = 100)
	start_time = models.DateTimeField()
	users = models.ManyToManyField(User)

	def to_json(self):
		return {
			"chat_name": self.chat_name,
			"start_time": str(self.start_time),
		}


class Message(models.Model):
	chat_id = models.ForeignKey(Chat)
	user_id = models.ForeignKey(User)
	message = models.TextField()
	post_time = models.DateTimeField()