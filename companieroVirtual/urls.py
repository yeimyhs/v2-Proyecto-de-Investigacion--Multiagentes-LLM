from rest_framework.routers import SimpleRouter

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path , re_path, reverse
from django.urls import path,include, re_path
from knox import views as knox_views
from .views import *
from companieroVirtual import views
from companieroVirtual import viewsTemplates

from rest_framework.routers import DefaultRouter
router = SimpleRouter()
#router.register(r'user', views.UserViewSet)


urlpatterns = [
        path("chat/", chat_with_gemini, name="chat"),
        path("", viewsTemplates.chat_page, name="chat_page"), 
        #path("w", chat_pagew, name="chat_page"), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'conversations', ConversationViewSet)
router.register(r'knowledge-topics', KnowledgeTopicLearnedViewSet)
router.register(r'sub-knowledge', SubKnowledgeViewSet)
router.register(r'generated-by', GeneratedByViewSet)

urlpatterns += router.urls

