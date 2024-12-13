from rest_framework.routers import SimpleRouter

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path , re_path, reverse
from django.urls import path,include, re_path
from knox import views as knox_views
from .views import *
from companieroVirtual import views
from companieroVirtual import viewsTemplates

router = SimpleRouter()
#router.register(r'user', views.UserViewSet)


urlpatterns = [
        path("chat/", chat_with_gemini, name="chat"),
        path("", viewsTemplates.chat_page, name="chat_page"), 
        #path("w", chat_pagew, name="chat_page"), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls

