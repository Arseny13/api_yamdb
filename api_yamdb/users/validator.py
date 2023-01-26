from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def username_value_not_me(value):
    """Производит валидацию имени пользователя."""
    if value == 'me':
        raise ValidationError(
            _("%(value)s не может быть 'me'."),
            params={'value': value},
        )
