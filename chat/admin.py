from django.contrib import admin

from django.contrib.auth.models import User
from models import *

class ChatAdmin(admin.ModelAdmin):
    fields = ['chat_name', 'start_time']

admin.site.register(Chat, ChatAdmin)


class MessageAdmin(admin.ModelAdmin):
    fields = ['user_id', 'chat_id', 'message', 'post_time']

admin.site.register(Message, MessageAdmin)