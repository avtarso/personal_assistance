import json
from django.core.management.base import BaseCommand
from quotes.models import Author, Tag, Quote
from users.models import User

class Command(BaseCommand):
    help = 'Load quotes from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data:
                author_name = item['author']
                author, created = Author.objects.get_or_create(name=author_name)
                tags = item['tags']
                tag_objects = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]
                quote_text = item['quote']
                quote = Quote.objects.create(text=quote_text, author=author)
                quote.tags.set(tag_objects)
                quote.save()
        self.stdout.write(self.style.SUCCESS('Successfully loaded quotes'))

