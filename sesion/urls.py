from rest_framework.routers import SimpleRouter
from sesion import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path , re_path, reverse
from django.urls import path,include, re_path
from knox import views as knox_views
from .views import LoginView

from sesion import viewsTemplates

router = SimpleRouter()
router.register(r'user', views.UserViewSet)
router.register(r'sessions', views.SessionViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'topics-requirement', views.TopicsRequirementViewSet)
router.register(r'learning-technique', views.LearningTechniqueViewSet)
router.register(r'recommended-techniques', views.RecommendedTechniquesViewSet)



urlpatterns = [
    path('userinfo/', views.UserInfoView.as_view(), name='userinfo'),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('register/', views.RegisterAPI.as_view(), name='register'),
    
    
    
    
    path('login_register_view/', viewsTemplates.login_register_view, name='register_log'),
    path('sesion_conf/<int:id>/', viewsTemplates.session_detail_view, name='session_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += router.urls