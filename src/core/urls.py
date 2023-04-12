from . import views
from django.urls import path

app_name = 'core' 


urlpatterns = [
    path('', views.login, name='home'),
    path('account/forgot-password/', views.forgot_password, name='forgotpassword'),
    path('account/signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lockscreen/', views.lockscreen, name='lockscreen'),
    path('dashboard/settings/', views.settings, name='settings'),
    path('dashboard/cadets/', views.cadets, name='cadets'),
    path('dashboard/cadet/profile/', views.cadet_profile, name='cadet_profile'),
    path('dashboard/cadet/messages/', views.cadet_messages, name='cadet_messages'),
    path('dashboard/cadet/taskboard/', views.cadet_taskboard, name='cadet_taskboard'),
    path('dashboard/cadet/logbook/', views.cadet_logbook, name='cadet_logbook'),
    path('dashboard/cadet/logbook/overview/', views.cadet_logbook_overview, name='cadet_logbook_overview'),
    path('dashboard/supervisors/', views.supervisors, name='supervisors_profile'),
    path('dashboard/timeline/', views.timeline, name='timeline'),
]
