from django.urls import path
from . import views

from . import views as core_views


app_name = 'users'
urlpatterns = [
    path('api/users/', views.users_list, name="users-page"),
    path('home/', views.home, name='home'),
    path('login/', core_views.Login.as_view(), name='login'),
    path('signup/', core_views.signup, name='signup'),
    path('account/<int:user_id>/', views.user_page, name='userpage'),
    path('account/<int:user_id>/avatar', views.avatar_form, name='avatar_form'),
]
