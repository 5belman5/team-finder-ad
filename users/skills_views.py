import json
from http import HTTPStatus

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from projects.models import Skill
from team_finder import constants


def skill_autocomplete(request):
    query = request.GET.get('q', '')
    skills = Skill.objects.filter(
        name__icontains=query
    ).order_by('name')[:constants.SKILLS_AUTOCOMPLETE_LIMIT]
    data = [{'id': s.id, 'name': s.name} for s in skills]
    return JsonResponse(data, safe=False)


def add_skill(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Unauthorized'},
            status=HTTPStatus.FORBIDDEN
        )

    user = request.user

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON'},
                status=HTTPStatus.BAD_REQUEST
            )

        skill_id = data.get('skill_id')
        name = data.get('name')

        created = False
        added = False
        skill = None

        if skill_id:
            skill = get_object_or_404(Skill, id=skill_id)
        elif name:
            skill, created = Skill.objects.get_or_create(name=name)

        if skill:
            if not user.skills.filter(id=skill.id).exists():
                user.skills.add(skill)
                added = True
            return JsonResponse({
                'id': skill.id,
                'name': skill.name,
                'created': created,
                'added': added
            })

    return JsonResponse(
        {'error': 'Invalid request'},
        status=HTTPStatus.BAD_REQUEST
    )


def remove_skill(request, skill_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Unauthorized'},
            status=HTTPStatus.FORBIDDEN
        )

    user = request.user
    skill = get_object_or_404(Skill, id=skill_id)

    if request.method == 'POST':
        if user.skills.filter(id=skill.id).exists():
            user.skills.remove(skill)
            return JsonResponse({'status': 'ok'})

    return JsonResponse(
        {'error': 'Invalid request'},
        status=HTTPStatus.BAD_REQUEST
    )
