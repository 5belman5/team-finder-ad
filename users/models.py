import io
import random
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from PIL import Image, ImageDraw, ImageFont

from team_finder import constants
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=constants.MAX_LENGTH_NAME)
    surname = models.CharField(max_length=constants.MAX_LENGTH_SURNAME)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(
        max_length=constants.MAX_LENGTH_PHONE,
        unique=True
    )
    github_url = models.URLField(blank=True, null=True)
    about = models.TextField(
        max_length=constants.MAX_LENGTH_ABOUT,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    skills = models.ManyToManyField(
        'projects.Skill',
        related_name='users',
        blank=True
    )

    favorites = models.ManyToManyField(
        'projects.Project',
        related_name='interested_users',
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"

    def save(self, *args, **kwargs):
        """
        Сохраняет пользователя, генерируя аватар, если он не установлен.
        """
        if not self.avatar:
            self.avatar = self.generate_avatar()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("users:user_detail", kwargs={"user_id": self.pk})

    def generate_avatar(self):
        """
        Генерирует аватарку с первой буквой имени пользователя.
        """
        size = constants.AVATAR_SIZE
        bg_color = (
            random.randint(50, 200),
            random.randint(50, 200),
            random.randint(50, 200)
        )
        img = Image.new('RGB', size, color=bg_color)
        draw = ImageDraw.Draw(img)

        letter = self.name[0].upper() if self.name else 'U'

        try:
            font = ImageFont.truetype(
                constants.AVATAR_FONT_NAME,
                constants.AVATAR_FONT_SIZE
            )
        except Exception:
            font = ImageFont.load_default()

        try:
            left, top, right, bottom = draw.textbbox(
                (0, 0), letter, font=font
            )
            w, h = right - left, bottom - top
        except AttributeError:
            w, h = draw.textsize(letter, font=font)

        draw.text(
            (
                (size[0] - w) / 2,
                (size[1] - h) / 2 - constants.AVATAR_ANCHOR_OFFSET
            ),
            letter,
            fill=constants.AVATAR_TEXT_COLOR,
            font=font
        )

        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        return ContentFile(
            buffer.getvalue(),
            name=f'avatar_{uuid.uuid4()}.png'
        )
