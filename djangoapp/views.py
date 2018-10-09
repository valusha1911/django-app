from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from absUser.models import User
from usersProjects.models import Project


def index(request, user_id):
    if request.user.is_authenticated:
        user = User.objects.get(pk=user_id)
        full = f'{user.first_name} {user.last_name}'
        proj = Project.objects.filter(users=user_id)
        list_proj = [project.title for project in proj]
        return render(request,
                      'users/index.html',
                      context={
                          'full_name': full,
                          'age': user.age,
                          'project': list_proj,
                          'projects': proj,
                      }
                      )
    return HttpResponseRedirect(reverse('users:login'))
