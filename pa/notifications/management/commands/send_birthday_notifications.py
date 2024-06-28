# notifications/management/commands/send_birthday_notifications.py

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from pa.contacts.models import Contact


class Command(BaseCommand):
    help = 'Send birthday notifications to users about their contacts'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        upcoming_birthdays = Contact.objects.filter(
            birthday__range=(today + timedelta(days=6), today + timedelta(days=7))
        )

        for contact in upcoming_birthdays:
            if contact.added_by and contact.added_by.email:
                send_mail(
                    'Upcoming Birthday Reminder',
                    f'Hi {contact.added_by.username},\n\n'
                    f'This is a reminder that your contact {contact.name} has a birthday in 7 days!\n\n'
                    'Best regards,\nYour Personal Assistant',
                    settings.EMAIL_HOST_USER,
                    [contact.added_by.email],
                    fail_silently=False,
                )

        self.stdout.write(self.style.SUCCESS('Successfully sent birthday notifications'))
