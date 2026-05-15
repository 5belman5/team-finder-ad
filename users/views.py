from django.contrib.auth import (
    get_user_model, login, logout, update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from projects.models import Skill
from .forms import LoginForm, PasswordChangeForm, ProfileEditForm, RegisterForm
from .service import get_paginated_objects

User = get_user_model()


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('projects:project_list')

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('projects:project_list')

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('projects:project_list')


def user_list(request):
    users_all = User.objects.prefetch_related('skills').all().order_by('id')
    active_skill = request.GET.get('skill')
    all_skills = Skill.objects.all().order_by('name')

    if active_skill:
        users_all = users_all.filter(skills__name=active_skill)

    users = get_paginated_objects(request, users_all)

    return render(request, 'users/participants.html', {
        'participants': users,
        'all_skills': all_skills,
        'active_skill': active_skill
    })


def user_detail(request, user_id):
    user_obj = get_object_or_404(
        User.objects.prefetch_related(
            'skills', 'owned_projects', 'participated_projects'
        ),
        id=user_id
    )
    return render(request, 'users/user-details.html', {'user': user_obj})


@login_required
def edit_profile(request):
    form = ProfileEditForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user
    )
    if form.is_valid():
        form.save()
        return redirect('users:user_detail', user_id=request.user.id)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    form = PasswordChangeForm(request.POST or None)
    if form.is_valid():
        user = request.user
        if user.check_password(form.cleaned_data['old_password']):
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)
            return redirect('users:user_detail', user_id=user.id)

        form.add_error('old_password', 'Неверный текущий пароль')

    return render(request, 'users/change_password.html', {'form': form})
