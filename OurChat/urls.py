from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import chat
from chat import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OurChat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'chat.views.index', name='index'),
	url(r'^create_user/$', 'chat.views.create_user', name='create_user'),
	url(r'^name/$', 'chat.views.name', name='name'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
