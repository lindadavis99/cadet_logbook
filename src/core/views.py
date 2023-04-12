from django.shortcuts import render



def dashboard(request):
    return render(request, 'core/dashboard.html', {})



def login(request):
    return render(request, 'core/login.html', {})



def signup(request):
    return render(request, 'core/signup.html', {})


def settings(request):
    return render(request, 'core/settings.html', {})


def lockscreen(request):
    return render(request, 'core/lockscreen.html', {})


def cadets(request):
    return render(request, 'core/cadets.html', {})


def cadet_profile(request):
    return render(request, 'core/profile.html', {})


def cadet_messages(request):
    return render(request, 'core/message.html', {})


def cadet_taskboard(request):
    return render(request, 'core/taskboard.html', {})


def cadet_logbook(request):
    return render(request, 'core/cadet_logbook.html', {})


def cadet_logbook_overview(request):
    return render(request, 'core/cadetlogbook_overview.html', {})


def supervisors(request):
    return render(request, 'core/supervisors.html', {})


def supervisor_profile(request):
    return render(request, 'core/supervisor_profile.html', {})


def settings(request):
    return render(request, 'core/settings.html', {})


def timeline(request):
    return render(request, 'core/timeline.html', {})


def forgot_password(request):
    return render(request, 'core/forgot_password.html', {})
