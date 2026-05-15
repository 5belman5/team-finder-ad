from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from projects.forms import ProjectForm
from projects.models import Project
from team_finder import constants
from users.service import get_paginated_objects


def project_list(request):
    projects_list = (
        Project.objects
        .select_related('owner')
        .prefetch_related('participants')
        .annotate(participants_count=Count('participants'))
        .all()
    )
    projects = get_paginated_objects(request, projects_list)

    favorite_project_ids = []
    if request.user.is_authenticated:
        favorite_project_ids = (
            request.user.favorites.values_list('id', flat=True)
        )

    return render(
        request,
        'projects/project_list.html',
        {
            'projects': projects,
            'favorite_project_ids': favorite_project_ids
        }
    )


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects
        .select_related('owner')
        .prefetch_related('participants')
        .annotate(participants_count=Count('participants')),
        id=project_id
    )
    return render(
        request,
        'projects/project-details.html',
        {'project': project}
    )


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect('projects:project_detail', project_id=project.id)

    return render(
        request,
        'projects/create-project.html',
        {'form': form, 'is_edit': False}
    )


@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('projects:project_detail', project_id=project.id)

    return render(
        request,
        'projects/create-project.html',
        {'form': form, 'is_edit': True}
    )


@login_required
def project_complete(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == 'POST' and project.status == constants.STATUS_OPEN:
        project.status = constants.STATUS_CLOSED
        project.save()
        return JsonResponse({
            'status': 'ok',
            'project_status': constants.STATUS_CLOSED
        })
    return JsonResponse(
        {'status': 'error'},
        status=HTTPStatus.BAD_REQUEST
    )


@login_required
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.status == constants.STATUS_CLOSED:
        return JsonResponse(
            {
                'status': 'error',
                'message': 'Нельзя присоединиться к закрытому проекту'
            },
            status=HTTPStatus.BAD_REQUEST
        )

    if request.method == 'POST':
        is_participant = project.participants.filter(
            id=request.user.id
        ).exists()
        if is_participant:
            project.participants.remove(request.user)
        else:
            project.participants.add(request.user)
        return JsonResponse({'status': 'ok', 'participant': not is_participant})

    return JsonResponse(
        {'status': 'error'},
        status=HTTPStatus.BAD_REQUEST
    )


@login_required
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        is_fav = request.user.favorites.filter(id=project.id).exists()
        if is_fav:
            request.user.favorites.remove(project)
        else:
            request.user.favorites.add(project)
        return JsonResponse({'status': 'ok', 'is_favorite': not is_fav})

    return JsonResponse(
        {'status': 'error'},
        status=HTTPStatus.BAD_REQUEST
    )


@login_required
def favorite_projects(request):
    projects_list = (
        request.user.favorites
        .select_related('owner')
        .prefetch_related('participants')
        .annotate(participants_count=Count('participants'))
        .all()
    )
    projects = get_paginated_objects(request, projects_list)
    favorite_project_ids = projects_list.values_list('id', flat=True)

    return render(
        request,
        'projects/favorite_projects.html',
        {
            'projects': projects,
            'favorite_project_ids': favorite_project_ids
        }
    )
