from . import views
from django.urls import path

app_name = 'core' 


urlpatterns = [
    path('', views.login, name='home'),
    path('account/forgot-password/', views.forgot_password, name='forgotpassword'),
    path('account/signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
