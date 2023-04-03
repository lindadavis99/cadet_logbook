from . import views
from django.urls import path

app_name = 'core' 


urlpatterns = [
    path('', views.login, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
]
