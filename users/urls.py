from django.urls import path

from . import skills_views, views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.user_list, name='user_list'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path(
        'skills/',
        skills_views.skill_autocomplete,
        name='skill_autocomplete'
    ),
    path('skills/add/', skills_views.add_skill, name='add_skill'),
    path(
        'skills/<int:skill_id>/remove/',
        skills_views.remove_skill,
        name='remove_skill'
    ),
]
