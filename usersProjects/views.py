from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q
from django.template.loader import render_to_string

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
def home(request):
    project_list = Project.objects.all()
    paginator = Paginator(project_list, 5)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    return render(request,
                  'projects/projects.html',
                  context={
                      'projects': projects,
                  }
                  )


@is_auth
def projects_table(request):
    search_text = request.GET.get('text', None)
    projects_sorted = request.GET.get('sort', None)
    page = request.GET.get('numPage', None)
    projects = Project.objects.all()
    if search_text:
        projects = projects.filter(Q(title__icontains=search_text)
                                   | Q(technologies__title__icontains=search_text)
                                   | Q(users__username__icontains=search_text)).distinct()
    if projects_sorted == '1':
        projects = projects.order_by('title')
    elif projects_sorted == '2':
        projects = projects.order_by('-title')

    paginator = Paginator(projects, 5)
    projects = paginator.get_page(page)
    print('page', page)
    print('sort', projects_sorted)
    rendered_table = render_to_string('projects/projects_table_list.html',
                                      context={'projects': projects, })
    rendered_pagination = render_to_string('projects/paginator.html',
                                           context={'projects': projects, })
    return JsonResponse({
        "projects_table": rendered_table,
        "pagination": rendered_pagination
    })


@is_auth
def detail(request, project_id):
    proj = Project.objects.get(pk=project_id)
    techn = Technology.objects.filter(
        projects=proj.id)
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
        return HttpResponseRedirect(reverse('users:userpage',
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
        return HttpResponseRedirect(reverse('users:userpage', args=[request.user.id]))
    elif request.method == "GET":
        return render(request,
                      'technologies/createTechnology.html',
                      context={
                          'projects': Project.objects.all(),
                      }
                      )
