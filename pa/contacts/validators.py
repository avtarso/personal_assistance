import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext


class EmailValidator:

    def __call__(self, value):
        if not re.match(r'^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$', value):
            raise ValidationError(
                gettext('Invalid email address format.'),
                code='invalid_email',
            )

    def get_help_text(self):
        return gettext('Enter a valid email address.')


class NameValidator:

    def __call__(self, value):
        if len(value) > 30:
            raise ValidationError(
                gettext('Too long name'),
                code='invalid_name'
            )

    def get_help_text(self):
        return gettext('Enter a valid name')


class PhoneValidator:

    def __call__(self, value):
        if not value.startswith("380") and len(value) != 12:
            raise ValidationError(
                gettext("Only Ukrainian numbers with country code '38XXXXXXXXXX'"),
                code='invalid_phone'
            )

    def get_help_text(self):
        return gettext('Enter a valid phone number')


class BirthdayValidator:

    def __call__(self, value):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
            raise ValidationError(
                gettext("Birthday format is 'YYYY-MM-DD'"),
                code='invalid_date'
            )

    def get_help_text(self):
        return gettext("Enter a valid date.")