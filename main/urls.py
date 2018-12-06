from django.urls import path
from django.contrib.auth.views import LoginView
from .views import allow_ip, validate_token

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html', success_url='/allow_ip')),
    path('allow_ip/', allow_ip),
    path('validate_token/', validate_token)
]
