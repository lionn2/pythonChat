from django.contrib import admin

from models import Chat, User

class ChatAdmin(admin.ModelAdmin):
    fields = ['chat_name', 'start_time']

admin.site.register(Chat, ChatAdmin)


class UserAdmin(admin.ModelAdmin):
    fields = ['name', 'date_registration']


admin.site.register(User, UserAdmin)