from . import views
from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)

app_name = 'core' 

urlpatterns = [
    path('', LoginView.as_view(template_name='core/login.html'), name='home'),
    path('account/auth/logout/', LogoutView.as_view(next_page='/lockscreen/'), name='logout'),
    path('account/auth/password-reset/', PasswordResetView.as_view(template_name='core/password_reset_form.html',
                                                           success_url='/account/auth/password-reset/done',
                                                           email_template_name='account/password_reset_email.html'),
                                                           name='forgotpassword'),
          
    path('account/auth/password-reset/done', PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
         name='password_reset_done'),
    path('account/auth/password-reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html',
                                          success_url='/account/auth/password-reset/complete/'),
         name='password_reset_confirm'),
         
    path('account/auth/password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),

    path('account/auth/sign-up/', views.Register.as_view(), name='signup'),
    path('account/auth/sign-up/cont/', views.Register2.as_view(), name='signup2'),
    path('account/auth/sign-up/completed/', views.SignUpCompleted.as_view(), name='signup_completed'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('lockscreen/', views.lockscreen, name='lockscreen'),
    path('dashboard/settings/', views.settings, name='settings'),
    path('dashboard/cadets/', views.cadets, name='cadets'),
    path('dashboard/cadet/<int:id>/profile/', views.cadet_profile, name='cadet_profile'),
    path('dashboard/cadet/messages/', views.cadet_messages, name='cadet_messages'),
    path('dashboard/cadet/taskboard/', views.cadet_taskboard, name='cadet_taskboard'),
    path('dashboard/cadet/logbook/', views.cadet_logbook, name='cadet_logbook'),
    path('dashboard/cadet/logbook/overview/', views.cadet_logbook_overview, name='cadet_logbook_overview'),
    path('dashboard/supervisors/', views.supervisors, name='supervisors_profile'),
    path('dashboard/timeline/', views.timeline, name='timeline'),
]
