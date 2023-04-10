from django.shortcuts import render



def dashboard(request):
    return render(request, 'core/dashboard.html', {})



def login(request):
    return render(request, 'core/login.html', {})



def signup(request):
    return render(request, 'core/signup.html', {})



def forgot_password(request):
    return render(request, 'core/forgot_password.html', {})
