from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from team_finder import constants
from .utils import GitHubUrlMixin, clean_phone_number

User = get_user_model()

PHONE_FORMAT_ERROR = (
    "Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(max_length=constants.MAX_LENGTH_PHONE)

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'phone', 'password')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned_phone = clean_phone_number(phone)

        if not cleaned_phone:
            raise forms.ValidationError(PHONE_FORMAT_ERROR)

        if User.objects.filter(phone=cleaned_phone).exists():
            raise forms.ValidationError("Этот номер телефона уже используется")

        return cleaned_phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProfileEditForm(GitHubUrlMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'avatar', 'about', 'phone', 'github_url')
        widgets = {
            'avatar': forms.FileInput(),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned_phone = clean_phone_number(phone)

        if not cleaned_phone:
            raise forms.ValidationError(PHONE_FORMAT_ERROR)

        if (User.objects.filter(phone=cleaned_phone)
                .exclude(pk=self.instance.pk).exists()):
            raise forms.ValidationError("Этот номер телефона уже используется")

        return cleaned_phone


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Текущий пароль"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Новый пароль"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Подтвердите новый пароль"
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 != new_password2:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'name': 'email'})
    )
