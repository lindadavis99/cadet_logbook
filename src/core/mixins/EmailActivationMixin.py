from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.http import HttpResponseServerError
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from ..token_generator import account_activation_token
from django.template import TemplateDoesNotExist, loader
from django.contrib.sites.shortcuts import get_current_site


class EmailActivationMixin:
    
    email_subject = 'Activate Your Account'
    
    def get_user(self):
        return User.objects.get(email=self.email)

    def init_email_activation(self, email):
        self.email = email
        self.user = self.get_user()
        self.current_site = get_current_site(self.request) 
        self.email_subject = self.email_subject
        self.domain = self.current_site.domain
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)
        
        
        '''
        self.activation_link = "http://" + self.domain +  reverse_lazy('account:activate', kwargs={
            'uidb64': self.uid, 
            'token': self.token
        })
        '''
        self.plain_message = render_to_string('account/activate_account.txt', {
            'user': self.user,
            'domain': self.domain,
            'uid': self.uid,
            'token': self.token,   
        })
        '''    
        self.html_message = render_to_string('account/activate_account.html', {
            'user': self.user,
            'activation_link': self.activation_link,
            'email': self.email
        })
        '''
    
    

    def send_activation_mail(self):
        
        send_activation_mail = send_mail(
            self.email_subject, 
            self.plain_message, 
            settings.EMAIL_HOST_USER,
            [self.email],
            #html_message= self.html_message
        )
            
        if send_activation_mail != 1:
            
            self.request.user.delete()
            try:
                template = loader.get_template('500.html')
                    
            except TemplateDoesNotExist:
                return HttpResponseServerError("Internal server error occured, Please contact uniabujanigeria@gmail.com")
                
            else:
                return HttpResponseServerError(template.render(request=self.request)) 

        else:
            return True 
        
        
class EmailActivationJsonResponseMixin(EmailActivationMixin):
        
    def send_activation_mail(self):
        email_sent = super().send_activation_mail()
        if email_sent:
            if self.request.is_ajax():
                data = {'result': 'Verification Email Sent!'}
                return JsonResponse(data) 
