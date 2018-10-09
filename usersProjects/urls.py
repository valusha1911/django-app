from django.urls import path
from . import views

# from . import views as core_views


app_name = 'projects'
urlpatterns = [
    path('projects/<int:project_id>/', views.detail, name = 'detail'),
    path('projects/addproject/', views.add_project, name='add project'),
    path('projects/addtechnology', views.add_technology, name='add technology'),
    path('api/projects/', views.projects_list, name='projects list'),
    path('api/technologies/', views.technologies_list, name='technologies list'),
    path('projects/', views.projects_page, name='projects'),
    path('projects/search/', views.projects_table, name='projects_search'),
]
