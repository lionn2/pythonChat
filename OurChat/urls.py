from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import chat
from chat import views


urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'chat.views.index', name='index'),
	url(r'^user_chats/', 'chat.views.user_chats', name='user_chats'),
	url(r'^create_user/$', 'chat.views.create_user', name='create_user'),
	url(r'^check_username/$', 'chat.views.check_username', name='check_username'),
	url(r'^login/$', 'chat.views.login', name='login'),
	url(r'^logout/$', 'chat.views.logout', name='logout'),
	url(r'^registration/$', 'chat.views.registration', name='registration'),
	url(r'^chat/(?P<id>\d+)/$', 'chat.views.chat', name='chat'),
	url(r'^chat/(?P<chat_id>\d+)/post_message/$', 'chat.views.post_message', name='post_message'),
	url(r'^chat/(?P<chat_id>\d+)/messages_from_id/$', 'chat.views.messages_from_id', name='messages_from_id'),
	url(r'^create_chat/$', 'chat.views.create_chat', name='create_chat'),
	url(r'^delete_chat/$', 'chat.views.delete_chat', name='delete_chat'),
	url(r'^delete_user_from_chat/', 'chat.views.delete_user_from_chat', name='delete_user_from_chat'),
	url(r'^chat/(?P<chat_id>\d+)/add_file/$', 'chat.views.add_file', name='add_file'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
