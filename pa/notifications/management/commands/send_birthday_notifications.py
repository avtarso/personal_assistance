from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, datetime
from collections import defaultdict
from pa.contacts.models import Contact

class Command(BaseCommand):
    help = 'Send birthday notifications to users about their contacts'

    def get_upcoming_birthdays(self, user, next_days):
        today = datetime.now().date()
        next_week = today + timedelta(days=next_days)

        if today.month == next_week.month:
            birthdays_within_range = Contact.objects.filter(
                user=user,
                birthday__month=today.month,
                birthday__day__gte=today.day,
                birthday__day__lte=next_week.day
            ).order_by('birthday__month', 'birthday__day')
        else:
            birthdays_within_range = Contact.objects.filter(
                user=user,
                birthday__month=today.month,
                birthday__day__gte=today.day
            ).exclude(
                birthday__month=today.month,
                birthday__day__gt=next_week.day
            ).exclude(
                birthday__month=next_week.month,
                birthday__day__lte=next_week.day
            ).order_by('birthday__month', 'birthday__day')

        if not birthdays_within_range.exists():
            self.stdout.write(self.style.WARNING(f"No contacts with birthdays in the next {next_days} days found."))
            return []

        contacts = [
            {
                'name': contact.full_name,
                'birthday': contact.birthday.strftime('%Y-%m-%d')
            }
            for contact in birthdays_within_range
        ]

        return contacts

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        start_date = today + timedelta(days=6)
        end_date = today + timedelta(days=7)

        self.stdout.write(self.style.NOTICE(f'Checking for upcoming birthdays in the range: {start_date} to {end_date}'))

        upcoming_birthdays = self.get_upcoming_birthdays(user=None, next_days=7)

        if not upcoming_birthdays:
            self.stdout.write(self.style.WARNING('No upcoming birthdays found for the next 7 days.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {len(upcoming_birthdays)} contacts with upcoming birthdays.'))

        user_contacts = defaultdict(list)
        for contact_info in upcoming_birthdays:
            try:
                contact = Contact.objects.get(full_name=contact_info['name'], birthday=datetime.strptime(contact_info['birthday'], '%Y-%m-%d').date())
                if contact.added_by and contact.added_by.email:
                    user_contacts[contact.added_by].append(contact)
                    self.stdout.write(self.style.NOTICE(f'Contact {contact.name} added to user {contact.added_by.username} list.'))
            except Contact.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Contact {contact_info["name"]} with birthday {contact_info["birthday"]} does not exist.'))

        if not user_contacts:
            self.stdout.write(self.style.WARNING('No users with email addresses found for notification.'))
            return

        for user, contacts in user_contacts.items():
            if user.email:
                self.stdout.write(self.style.NOTICE(f'Preparing to send email to {user.email}'))
                contacts_info = '\n'.join(
                    [f"{contact.name}: {contact.birthday.strftime('%Y-%m-%d')}" for contact in contacts]
                )
                result = send_mail(
                    'Upcoming Birthday Reminder',
                    f'Hi {user.username},\n\n'
                    f'This is a reminder that your contacts have upcoming birthdays in 7 days:\n\n'
                    f'{contacts_info}\n\n'
                    'Best regards,\nYour Personal Assistant',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                if result:
                    self.stdout.write(self.style.SUCCESS(f'Successfully sent birthday notification to {user.email}.'))
                else:
                    self.stdout.write(self.style.ERROR(f'Failed to send birthday notification to {user.email}.'))

        self.stdout.write(self.style.SUCCESS('Finished sending birthday notifications.'))
