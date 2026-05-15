from django.conf import settings
from django.db import models
from django.urls import reverse

from team_finder import constants


class Skill(models.Model):
    name = models.CharField(
        max_length=constants.MAX_LENGTH_SKILL_NAME,
        unique=True
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=constants.MAX_LENGTH_PROJECT_NAME)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField(blank=True, null=True)
    status = models.CharField(
        max_length=max(len(s[0]) for s in constants.STATUS_CHOICES),
        choices=constants.STATUS_CHOICES,
        default=constants.STATUS_OPEN
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "projects:project_detail",
            kwargs={"project_id": self.pk}
        )
