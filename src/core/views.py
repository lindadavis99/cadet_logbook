from django.db.models import Q
from django.contrib import messages
from . models import Profile, Cadetlogbook
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .forms import (
    UserRegistrationForm, SupervisorRegistrationForm, 
    CadetRegistrationForm, CadetLogbookModelForm,
    SearchForm
)
#from .token_generator import account_activation_token
from django.contrib.auth.decorators import login_required
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)


class Register(FormView):
    template_name = 'core/signup.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy("core:signup2")

    def form_valid(self, form):
        self.request.session['user_data'] = self.request.POST
        return super().form_valid(form)



class Register2(FormView):
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
 
    return render(request, 'core/cadets.html', {
        'profile':profile,
       
    })


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def delete_logbook_entry(request):
    if request.method == "POST" and is_ajax(request=request):
        logbook_id = request.POST.get('entry_id')
        print(logbook_id)
        logbook_entry = Cadetlogbook.objects.get(id=logbook_id)
        logbook_entry.delete()
        return JsonResponse({"message": "Logbook Entry Successfully Deleted"}, status=200)

    else:
        return JsonResponse({'errors' : 'Failed to process request, please try again later'}, status=404)

@login_required
def update_logbook_entry(request, id):
    profile = get_object_or_404(Profile, user=request.user)
    logbook_instance = get_object_or_404(Cadetlogbook, id=id)
    form = CadetLogbookModelForm(request.POST or None, instance=logbook_instance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Logbook Successfully Updated")
            return HttpResponseRedirect("/dashboard/cadet/logbook/")

    return render(request, 'core/update_logbook.html', {
        'form' : form, 
        'profile' : profile,
        'logbook_instance' : logbook_instance.id
    })


@login_required
def cadet_profile(request):
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



def is_valid_queryparam(param):
    return param != '' and param is not None

@login_required
def cadet_logbook(request):
    cadet_logbooks = None
    search_form =  SearchForm(request.GET)
    keyword = request.GET.get('keyword') 
    profile = get_object_or_404(Profile, user=request.user)

    if profile.account_type == 'cadet':
        cadet_logbooks = Cadetlogbook.objects.filter(user=request.user)
    
    else: 
        cadet_logbooks = Cadetlogbook.objects.all() 

    if is_valid_queryparam(keyword):
        cadet_logbooks = Cadetlogbook.published.filter(
            Q(work_title__icontains=keyword)|
            Q(description_of_work__icontains=keyword) |
            Q(user__first_name__icontains=keyword) | 
            Q(user__last_name__icontains=keyword) 
        ).distinct()

    
    paginator = Paginator(cadet_logbooks, 2)
    page = request.GET.get('page')

    try:
        cadet_logbooks = paginator.page(page)

    except PageNotAnInteger:
        cadet_logbooks = paginator.page(1) 

    except EmptyPage:
        cadet_logbooks = paginator.page(paginator.num_pages)

    return render(request, 'core/cadet_logbook.html', {
        'profile': profile,
        'page': page,
        'search_form': search_form,  
        'cadet_logbooks' : cadet_logbooks
    })

@login_required
def createlogbook(request):
    profile = get_object_or_404(Profile, user=request.user)
    form = CadetLogbookModelForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Logbook Successfully Created")
            return HttpResponseRedirect("/dashboard/cadet/logbook/")
        else:
            messages.error(request, "Logbook failed to save")
            return HttpResponseRedirect("/dashboard/cadet/logbook/")

    return render(request, 'core/create_logbook.html', {
        'profile': profile,
        'form' : form
    })


@login_required
def cadet_logbook_overview(request, id):
    profile = get_object_or_404(Profile, user=request.user)
    cadet_logbook = get_object_or_404(Cadetlogbook, pk=id)
    return render(request, 'core/cadetlogbook_overview.html', {
        'profile': profile,
        'cadet_logbook' : cadet_logbook 
    })

@login_required
def supervisors(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'core/supervisors.html', {
        'profile': profile
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
