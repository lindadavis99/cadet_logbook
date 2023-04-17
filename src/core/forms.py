import re
from .models import Cadetlogbook
from django import forms
from django.contrib.auth.models import User 

ACCOUNT_TYPE = (
    ('supervisor', 'Supervisor'),
    ('cadet', 'Cadet')
)


GENDER = (
    ('male', 'Male'),
    ('female', 'Female')
)


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(required=True, max_length=50)
    first_name = forms.CharField(required=True, max_length=20)
    last_name = forms.CharField(required=True, max_length=20)
    gender = forms.CharField(required=True, max_length=20, widget=forms.Select(choices=GENDER))
    account_type = forms.CharField(required=True, max_length=20, widget=forms.Select(choices=ACCOUNT_TYPE))
    
    def clean_email(self):
        cd = self.cleaned_data
        email = cd['email']
        try:                                                     
            User.objects.get(email=email)
            raise forms.ValidationError("Sorry this email id already exists.")
        except User.DoesNotExist:
            pass

        return email


class RegistrationForm2(forms.Form):
    custom_error_message = str()
    username = forms.CharField(required=True)
    password = forms.CharField(min_length=10, max_length=100, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=10, max_length=100, required=True, widget=forms.PasswordInput)

    def clean_username(self):
        cd = self.cleaned_data
        username = cd['username']
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(self.custom_error_message)
        except User.DoesNotExist:
            pass

        return username
    

    def clean(self):
        super().clean()
        cd = self.cleaned_data
        password = cd['password']
        password2 = cd['password2']
        symbol_regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        uppercase_regex = re.compile('[A-Z]')
        if password and password2:
            if (symbol_regex.search(password) is None) or (uppercase_regex.search(password) is None):
                raise forms.ValidationError("passwords must contain at least one uppercase and a symbol character.")
            else:
                if cd['password'] != cd['password2']:
                    raise forms.ValidationError("Passwords don't match.")


class SupervisorRegistrationForm(RegistrationForm2):
    custom_error_message = 'Sorry This Staff Id Already Exists.'



class CadetRegistrationForm(RegistrationForm2):
    custom_error_message = 'Sorry This Reg No Already Exists. '



class CadetLogbookModelForm(forms.ModelForm):
    
    class Meta:
        model = Cadetlogbook
        fields = ['work_title','department', 'description_of_work', 'end_date']


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=50, required=True, strip=True)


class SupervisorCommentModelForm(forms.ModelForm):

    class Meta:
        model = Cadetlogbook
        fields = ['work_status', 'comment']