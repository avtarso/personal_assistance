# notifications/management/commands/send_birthday_notifications.py

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from pa.contacts.models import Contact
from collections import defaultdict


class Command(BaseCommand):
    help = 'Send birthday notifications to users about their contacts'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        upcoming_birthdays = Contact.objects.filter(
            birthday__range=(today + timedelta(days=6), today + timedelta(days=7))
        )

        user_contacts = defaultdict(list)
        for contact in upcoming_birthdays:
            if contact.added_by and contact.added_by.email:
                user_contacts[contact.added_by].append(contact)

        for user, contacts in user_contacts.items():
            if user.email:
                contacts_info = '\n'.join(
                    [f"{contact.name}: {contact.birthday.strftime('%Y-%m-%d')}" for contact in contacts]
                )
                send_mail(
                    'Upcoming Birthday Reminder',
                    f'Hi {user.username},\n\n'
                    f'This is a reminder that your contacts have upcoming birthdays in 7 days:\n\n'
                    f'{contacts_info}\n\n'
                    'Best regards,\nYour Personal Assistant',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

        self.stdout.write(self.style.SUCCESS('Successfully sent birthday notifications'))
