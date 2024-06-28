import os
from datetime import datetime

import django

# Installing the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pa.settings")
django.setup()

from django.contrib.auth.models import User
from notes.models import Note, Tag as NoteTag
from contacts.models import Contact


username = "user"
password = "user"
file_path = 'first_start.py'

notes = [
    {
        "name": "Data Science",
        "description": "Our next course module",
        "tags": ["next", "module"]
    },
    {
        "name": "Core",
        "description": "Our previous course module",
        "tags": ["previous", "module"]
    }
]

contacts = [
    {
        "name": "Billy Jinn",
        "address": "ul. Pushkina, dom Kolotushkina",
        "phone": "88005553535",
        "email": "billy_jinn@gmail.com",
        "birthday": datetime(year=1997, month=7, day=14)
    },
    {
        "name": "Petro Mostavchuk",
        "address": "m. Lviv",
        "phone": "380951488228",
        "email": "p_mostavchuk@gmail.com",
        "birthday": datetime(year=1995, month=1, day=1)
    }
]


def import_data(user):

    for contact_data in contacts:
        user = User.objects.get(username=user)
        Contact.objects.create(
            name=contact_data["name"],
            address=contact_data["address"],
            phone=contact_data["phone"],
            email=contact_data["email"],
            birthday=contact_data["birthday"],
            added_by=user
        )


    for note_data in notes:
        user = User.objects.get(id=1)
        note = Note.objects.create(
            name=note_data["name"],
            description=note_data["description"],
            added_by=user
        )

        for tag_name in note_data["tags"]:
            tag, _ = NoteTag.objects.get_or_create(name=tag_name)
            note.tags.add(tag)


    print("Data imported successfully!")


def create_user(username, password):

    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password=password)
        print(f"User '{username}' created successfully!")
    else:
        print(f"User '{username}' already exists.")


if __name__ == "__main__":

    if not os.path.exists(file_path):
        # Create empty file. Only for testing and demonstrate
        with open(file_path, 'w') as file:
            pass
        create_user(username, password)
        import_data(username)
