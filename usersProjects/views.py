from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q
from django.template.loader import render_to_string

from absUser.models import User
from absUser.views import is_auth
from .models import Project, Technology, Like
from .forms import ProjectForm, TechnologyForm


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
                  })


def likes(request):
    if request.method == "POST":
        like_count = int(request.POST.get('like'))
        proj_id = request.POST.get('projectId')

        obj, created = Like.objects.get_or_create(
            users_id__id=request.user.id,
            projects_id__id=proj_id,
        )
        if created:
            like_count += 1
            obj.users_id.add(request.user.id)
            obj.projects_id.add(proj_id)
            obj.save()
        else:
            like_count -= 1
            obj.delete()
    return render(request,
                  'projects/projects_feed.html',
                  context={
                      'projects': Project.objects.all(),
                  })


def projects_feed(request):
    search_text = request.GET.get('text', None)
    page = request.GET.get('numPage', None)
    projects = Project.objects.all()
    if search_text:
        projects = projects.filter(Q(title__icontains=search_text)
                                   | Q(description__icontains=search_text)
                                   | Q(technologies__title__icontains=search_text)
                                   | Q(users__first_name__icontains=search_text)
                                   | Q(users__last_name__icontains=search_text)).distinct()
    paginator = Paginator(projects, 5)
    projects = paginator.get_page(page)
    rendered_body = render_to_string('projects/projects_feed.html',
                                     context={
                                         'projects': projects,
                                     })
    rendered_pagination = render_to_string('projects/paginator.html',
                                           context={
                                               'projects': projects,
                                           })
    return JsonResponse({
        "projects_body": rendered_body,
        "pagination": rendered_pagination
    })


@is_auth
def detail(request, project_id):
    project = Project.objects.get(pk=project_id)
    technologies = Technology.objects.filter(
        projects=project.id)
    return render(request,
                  'projects/detail.html',
                  context={
                      'project': project,
                      'technologies': ', '.join([tech.title for tech in technologies]),
                  })


@is_auth
def projects_list(request):
    return render(request,
                  'projects/projectslist.html',
                  context={
                      'projects': Project.objects.all(),
                  })


@is_auth
def technologies_list(request):
    return render(request,
                  'technologies/technologieslist.html',
                  context={
                      'technologies': Technology.objects.all(),
                  })


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
                      })


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
                      })
