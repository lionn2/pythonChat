from django.contrib import admin

from models import *

class ChatAdmin(admin.ModelAdmin):
    fields = ['chat_name', 'start_time']

admin.site.register(Chat, ChatAdmin)


class UserAdmin(admin.ModelAdmin):
    fields = ['name', 'date_registration']


admin.site.register(User, UserAdmin)


class MessageAdmin(admin.ModelAdmin):
    fields = ['user_id', 'chat_id', 'message', 'post_time']

admin.site.register(Message, MessageAdmin)