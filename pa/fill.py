import os
from datetime import datetime

import django

# Installing the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pa.settings")
django.setup()

from django.contrib.auth.models import User
from quotes.models import Author, Quote, Tag
from notes.models import Note, Tag as NoteTag
from contacts.models import Contact

username = "user"
password = "user"

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

authors = [
    {
        "fullname": "Rust Cohle",
        "born_date": "July 31, 1965",
        "born_location": "USA",
        "description": "description 1",
    },
    {
        "fullname": "Gregory House",
        "born_date": "July 31, 1965",
        "born_location": "London, England",
        "description": "description 2",
    },
]

quotes = [
    {
        "tags": ["divine", "person"],
        "author": "Rust Cohle",
        "quote": "“If the only thing keeping a person decent is the expectation of divine reward then, brother, that person is a piece of s***. And I’d like to get as many of them out in the open as possible. You gotta get together and tell yourself stories that violate every law of the universe just to get through the goddamn day? What’s that say about your reality?”",
    },
    {
        "tags": ["deserve", "People"],
        "author": "Gregory House",
        "quote": "“People don't get what they deserve. They just get what they get. There's nothing any of us can do about it.”",
    },
]


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%B %d, %Y").date()
    except ValueError:
        return None


def import_data(user):
    for author_data in authors:
        author, created = Author.objects.get_or_create(
            fullname=author_data["fullname"],
            born_date=parse_date(author_data["born_date"]),
            born_location=author_data["born_location"],
            description=author_data.get("description", ""),
            added_by=None,
        )

    for quote_data in quotes:
        author = Author.objects.get(fullname=quote_data["author"])
        quote = Quote.objects.create(
            text=quote_data["quote"], author=author, added_by=None
        )

        for tag_name in quote_data["tags"]:
            tag, created = Tag.objects.get_or_create(
                name=tag_name, defaults={"added_by": None}
            )
            quote.tags.add(tag)


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

file_path = 'first_start.py'

if __name__ == "__main__":

    if not os.path.exists(file_path):
        # Create empty file. Only for testing and demonstrate
        with open(file_path, 'w') as file:
            pass
        create_user(username, password)
        import_data(username)

