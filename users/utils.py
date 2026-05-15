from django import forms

from team_finder import constants


class GitHubUrlMixin:
    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and constants.GITHUB_DOMAIN not in url:
            raise forms.ValidationError(
                f"Ссылка должна вести на {constants.GITHUB_DOMAIN}"
            )
        return url


def clean_phone_number(phone):
    """
    Вспомогательная функция для очистки и валидации номера телефона.
    """
    digits = "".join([c for c in phone if c.isdigit()])

    if phone.startswith('+'):
        if not (phone.startswith('+7') and len(digits) == 11):
            return None
    else:
        if not (digits.startswith('8') and len(digits) == 11):
            return None

    return '+7' + digits[1:]
