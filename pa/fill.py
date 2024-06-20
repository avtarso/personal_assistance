import os
from datetime import datetime

import django

# Установка Django окружения
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pa.settings")
django.setup()

from django.contrib.auth.models import User
from quotes.models import Author, Quote, Tag

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


def import_data():
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

    print("Data imported successfully!")


def create_user():
    username = "user"
    password = "user"

    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password=password)
        print(f"User '{username}' created successfully!")
    else:
        print(f"User '{username}' already exists.")


if __name__ == "__main__":
    import_data()
    create_user()
