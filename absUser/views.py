from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash

from usersProjects.models import Project
from .models import User
from .forms import SignUpForm


def is_auth(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            print('here2')
            return HttpResponseRedirect(reverse('users:login'))
    return wrapper


class Login(LoginView):
    template_name = 'auth/signin.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('projects:home'))
        else:
            return super().dispatch(request, *args, **kwargs)


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('projects:home'))
    else:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                raw_pass = form.cleaned_data.get('password1')
                raw_username = form.cleaned_data.get('username')
                user = authenticate(username=raw_username, password=raw_pass)
                login(request, user)
                return HttpResponseRedirect(reverse('users:home'))
        elif request.method == "GET":
            form = SignUpForm()
        return render(request, 'auth/signup.html')


@is_auth
def user_page(request, user_id):
    try:
        form = User.objects.get(id=user_id)
        if request.method == "POST":
            form.username = request.POST.get('username')
            form.first_name = request.POST.get('first_name')
            form.last_name = request.POST.get('last_name')
            form.age = request.POST.get('age')
            form.email = request.POST.get('email')
            if request.POST.get('newPassword'):
                if request.POST.get('newPassword') == request.POST.get('retryPassword'):
                    form.set_password(request.POST.get('newPassword'))
                    update_session_auth_hash(request, form)
            form.save()
            return render(request,
                          'users/userpage.html',
                          context={
                              'user_page': User.objects.get(id=user_id),
                              'projects': Project.objects.filter(users=request.user.id),
                          })
        elif request.method == "GET":
            return render(request,
                          'users/userpage.html',
                          context={
                              'user_page': User.objects.get(id=user_id),
                              'projects': Project.objects.filter(users=request.user.id),
                          })
    except form.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def avatar_form(request, user_id):
    form = User.objects.get(id=user_id)
    if request.method == "POST":
        form.avatar = request.FILES['avatar']
        form.save()
        return render(request,
                      'users/userpage.html',
                      context={
                          'user_page': User.objects.get(id=user_id),
                          'projects': Project.objects.filter(users=request.user.id),
                      })
    return render(request, 'avatarform.html')


@is_auth
def users_list(request):
    return render(request,
                  'users/users.html',
                  context={
                      'user_list': User.objects.all(),
                  })
