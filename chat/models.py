from django.db import models
from django.contrib.auth.models import User
import json

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
			"user": self.user_id.username,
			"message": self.message,
			"post_time": str(self.post_time),
		}

def query_to_json(data):
	mess = []	
	for m in data:
		mess.append(m.to_json())
 	return json.dumps(mess)


class Upload(models.Model):
    pic = models.ImageField("Image", upload_to="images/")    
    upload_date=models.DateTimeField(auto_now_add =True)

from django.forms import ModelForm

# FileUpload form class.
class UploadForm(ModelForm):
    class Meta:
        model = Upload