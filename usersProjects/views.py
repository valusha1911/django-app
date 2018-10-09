from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q

from absUser.models import User
from .models import Project, Technology
from .forms import ProjectForm, TechnologyForm


def is_auth(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            print('here2')
            return HttpResponseRedirect(reverse('users:login'))
    return wrapper


def preventAuthIfUserExist(func):
    def wrapper(request, *args, **kwargs):
        # request.hasattr('user') ? request.user :  args
        # print('args1', dir(args[0]))
        # print('asd0', request.user)
        # user = request.user or args[0].user
        # if user and user.is_authenticated:
        # print('res', dir(request, 'user'))
        if hasattr(request, 'user'):
            print('here1')
            return HttpResponseRedirect(reverse('users:home'))
        else:
            return func(request, *args, **kwargs)
    return wrapper


@is_auth
def projects_page(request):
    projects = Project.objects.all()
    return render(request,
                  'projects/projects.html',
                  context={
                      'projects': projects,
                  }
                  )


@is_auth
def projects_table(request):
    searchText = request.GET.get('text')
    projects = Project.objects.all()  # pylint: disable=E1101
    if searchText:
        projects = projects.filter(Q(title__icontains=searchText)
                                   | Q(technologies__title__icontains=searchText)
                                   | Q(users__username__icontains=searchText)).distinct()

    return render(request,
                  'projects/projects_table_list.html',
                  context={
                      'projects': projects,
                  }
                  )


@is_auth
def detail(request, project_id):
    proj = Project.objects.get(pk=project_id)  # pylint: disable=E1101
    techn = Technology.objects.filter(
        projects=proj.id)  # pylint: disable=E1101
    return render(request,
                  'projects/detail.html',
                  context={
                      'title': proj,
                      'techn': ', '.join([tech.title for tech in techn]),
                      'users': proj.users.all()
                  }
                  )


@is_auth
def projects_list(request):
    return render(request,
                  'projects/projectslist.html',
                  context={
                      'projects': Project.objects.all(),
                  }
                  )


@is_auth
def technologies_list(request):
    return render(request,
                  'technologies/technologieslist.html',
                  context={
                      'technologies': Technology.objects.all(),
                  }
                  )


@is_auth
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('user-page',
                                            args=[request.user.id]))
    elif request.method == "GET":
        technologies = Technology.objects.all()
        users = User.objects.all()
        return render(request,
                      'projects/createProject.html',
                      context={
                          'users': users,
                          'techs': technologies,
                      }
                      )


@is_auth
def add_technology(request):
    if request.method == "POST":
        form = TechnologyForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('user-page', args=[request.user.id]))
    elif request.method == "GET":
        return render(request,
                      'technologies/createTechnology.html',
                      context={
                          'projects': Project.objects.all(),
                      }
                      )
