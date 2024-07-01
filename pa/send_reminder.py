#/pa/send_reminder.py
#====run
# cd pa
# python send_reminder.py


import os
from datetime import date, timedelta
from collections import defaultdict

import django
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pa.settings")
django.setup()

from contacts.models import Contact


def send_birthday_reminders():
    today = date.today()
    end_date = today + timedelta(days=7)

    upcoming_birthdays = Contact.objects.filter(
        birthday__isnull=False,
        birthday__month__in=[today.month, end_date.month],
        birthday__day__gte=today.day if today.month == end_date.month else 1,
        birthday__day__lte=end_date.day if today.month == end_date.month else 31
    )

    if not upcoming_birthdays.exists():
        print("No upcoming birthdays found.")
        return

    contacts_by_user = defaultdict(list)
    for contact in upcoming_birthdays:
        if contact.added_by:
            contacts_by_user[contact.added_by].append(contact)

    for user, contacts in contacts_by_user.items():
        contact_details = "\n".join(
            f"{contact.name}: {contact.birthday.strftime('%d-%m-%Y')}" for contact in contacts
        )

        subject = "Upcoming Birthdays Reminder"
        message = f"Dear {user.username},\n\n" \
                  f"We wanted to remind you about the upcoming birthdays of your contacts:\n\n" \
                  f"{contact_details}\n\n" \
                  f"Don't forget to celebrate with them!\n\n" \
                  f"Best regards,\nYour Personal Assistant\n\n" \
                  f"P.S. If you haven't already, check out our app for more details!"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

    print("Birthday reminders sent successfully.")


if __name__ == "__main__":
    send_birthday_reminders()
