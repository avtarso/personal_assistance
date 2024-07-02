#/pa/send_reminder.py
#====run
# cd pa
# python send_reminder.py


import os
from datetime import datetime

import django

# Installing the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pa.settings")
django.setup()

from django.contrib.auth.models import User
from notes.models import Note, Tag as NoteTag
from contacts.models import Contact


from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from collections import defaultdict

today = date.today()
end_date = today + timedelta(days=7)

upcoming_birthdays = Contact.objects.filter(
    birthday__isnull=False,
    birthday__month__in=[today.month, end_date.month],
    birthday__day__gte=today.day if today.month == end_date.month else 1,
    birthday__day__lte=end_date.day if today.month == end_date.month else 31
)

contacts_by_user = defaultdict(list)
for contact in upcoming_birthdays:
    if contact.added_by:
        contacts_by_user[contact.added_by].append(contact)
        print(contact)


def send_birthday_reminders():
    for user, contacts in contacts_by_user.items():
        contact_details = "\n".join(
            f"{contact.name}: {contact.birthday.strftime('%d-%m-%Y')}, {contact.phone}, {contact.email}" for contact in contacts
        )
        
        subject = "Upcoming Birthdays Reminder"
        message = f"Dear {user.username},\n\n" \
                  f"The following contacts have birthdays coming up in the next week:\n\n" \
                  f"{contact_details}\n\n" \
                  f"You can see full information on https://personalassistance-production.up.railway.app/contacts/\n\n" \
                  f"Best regards,\nYour Personal Assistance"
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


if __name__ == "__main__":
    print(send_birthday_reminders())



