from django.urls import path
from . import views


app_name = 'projects'
urlpatterns = [
    path('projects/<int:project_id>/', views.detail, name='detail'),
    path('projects/addproject/', views.add_project, name='add project'),
    path('projects/addtechnology', views.add_technology, name='add technology'),
    path('api/projects/', views.projects_list, name='projects list'),
    path('api/technologies/', views.technologies_list, name='technologies list'),
    path('projects/search/', views.projects_feed, name='projects_search'),
    path('projects/sort/', views.projects_feed, name='projects_sort'),
    path('home/', views.home, name='home'),
    path('projects/likes/', views.likes, name='likes'),
]
