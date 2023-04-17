from . models import Profile
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import FormView 
from django.views.generic import TemplateView
from .mixins.EmailActivationMixin import EmailActivationMixin
from .forms import (UserRegistrationForm, SupervisorRegistrationForm, CadetRegistrationForm)
#from .token_generator import account_activation_token
from django.contrib.auth.decorators import login_required


class Register(FormView):
    template_name = 'core/signup.html'
    form_class = UserRegistrationForm 
    success_url = reverse_lazy("core:signup2")
         
    def form_valid(self, form):
        self.request.session['user_data'] = self.request.POST 
        return super().form_valid(form) 


    
class Register2(EmailActivationMixin, FormView):
    custom_text_value = str() 
    template_name = 'core/signup2.html'
    success_url = reverse_lazy("core:signup_completed")    
    
    def get_form_class(self):
        if self.request.session['user_data'].get('account_type').upper() == 'Cadet':
            self.form_class = CadetRegistrationForm
            self.custom_text_value = "Cadet No"
              
        else:
            self.form_class = SupervisorRegistrationForm 
            self.custom_text_value = "Supervisor No"
            
        return super().get_form_class()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session['user_data'].get('email')
        context['account_type'] = self.request.session['user_data'].get('account_type')
        context['form'] = self.get_form()
        context['custom_text_value'] = self.custom_text_value
        return context
    
    def form_valid(self, form):
        email = self.request.session['user_data'].get('email')
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = User.objects.create_user(username, email, password)
        user.first_name = self.request.session['user_data'].get('first_name')
        user.last_name = self.request.session['user_data'].get('last_name')
        user.is_active = True
        profile = Profile()
        profile.user = user
        profile.account_type = self.request.session['user_data'].get('account_type')
        profile.gender = self.request.session['user_data'].get('gender')            
        user.save()
        profile.save()
        return super().form_valid(form)
       # self.init_email_activation(email)
       # self.send_activation_mail() 
        
        
class  SignUpCompleted(TemplateView):
    template_name = 'core/signup_completed.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session['user_data'].get('email')
        return context


@login_required    
def dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)  

    if profile.account_type == 'supervisor':
        return render(request, 'core/supervisor_admin_dashboard.html', {
            'profile' : profile
        })
    
    else:
        return render(request, 'core/cadet_admin_dashboard.html', {
            'profile' : profile
        })


@login_required
def settings(request):
    profile = get_object_or_404(Profile, user=request.user) 
    return render(request, 'core/settings.html', {
        'profile': profile
    })


def lockscreen(request):
    return render(request, 'core/lockscreen.html', {})

@login_required
def cadets(request):
    profile = get_object_or_404(Profile, user=request.user)
    cadets = Profile.objects.filter(account_type='cadet')  
    return render(request, 'core/cadets.html', {
        'profile':profile,
        'cadets' : cadets 
    })

@login_required
def cadet_profile(request, id):
    profile = get_object_or_404(Profile, user=request.user)  
    return render(request, 'core/profile.html', {
        'profile':profile
    })

@login_required
def cadet_messages(request):
    profile = get_object_or_404(Profile, user=request.user)  
    return render(request, 'core/message.html', {
        'profile':profile
    })

@login_required
def cadet_taskboard(request):
    profile = get_object_or_404(Profile, user=request.user)  
    return render(request, 'core/taskboard.html', {
        'profile':profile
    })

@login_required
def cadet_logbook(request):
    profile = get_object_or_404(Profile, user=request.user)  
    return render(request, 'core/cadet_logbook.html', {
        'profile': profile
    })

@login_required
def cadet_logbook_overview(request):
    profile = get_object_or_404(Profile, user=request.user)  
    return render(request, 'core/cadetlogbook_overview.html', {
        'profile': profile
    })

@login_required
def supervisors(request):
    profile = get_object_or_404(Profile, user=request.user)  
    supervisors = Profile.objects.filter(account_type='supervisor')  
    return render(request, 'core/supervisors.html', {
        'profile': profile,
        'supervisors' : supervisors
    })

@login_required
def supervisor_profile(request):
    profile = get_object_or_404(Profile, user=request.user)  
    return render(request, 'core/supervisor_profile.html', {
        'profile': profile
    })


@login_required
def timeline(request):
    profile = get_object_or_404(Profile, user=request.user)  
    return render(request, 'core/timeline.html', {
        'profile':profile
    })


def forgot_password(request):
    return render(request, 'core/forgot_password.html', {})
