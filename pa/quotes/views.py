import json

from dateutil import parser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuthorForm, QuoteForm, TagForm, UploadFileForm
from .models import Author, Quote, Tag, UploadFile


def main_page(request):
    return render(request, "quotes/index.html")


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.added_by = request.user
            author.save()
            return redirect("quotes:author_list")
    else:
        form = AuthorForm()
    return render(request, "quotes/add_author.html", {"form": form})


@login_required
def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.added_by = request.user
            tag.save()
            return redirect("quotes:tag_list")
    else:
        form = TagForm()
    return render(request, "quotes/add_tag.html", {"form": form})


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.added_by = request.user
            quote.save()
            form.save_m2m()  # Save many-to-many data
            return redirect("quotes:quote_list")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})


def author_list(request):
    authors = Author.objects.all().order_by("fullname")
    return render(request, "quotes/author_list.html", {"authors": authors})


def top_10_tag_list(request):
    tags_with_counts = Tag.objects.annotate(num_quotes=Count("quote")).order_by(
        "-num_quotes"
    )[:10]
    context = {
        "tags_with_counts": tags_with_counts,
    }
    return render(request, "quotes/index.html", context)


def tag_list(request):
    tags_with_counts = Tag.objects.annotate(num_quotes=Count("quote")).order_by("name")
    context = {
        "tags_with_counts": tags_with_counts,
    }
    return render(request, "quotes/tag_list.html", context)


def tag_quotes(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    quotes = Quote.objects.filter(tags=tag)
    return render(
        request, "quotes/tag_quotes.html", {"quotes": quotes, "tag_name": tag.name}
    )


def quote_list(request):
    quotes = Quote.objects.all().order_by("-id")
    return render(request, "quotes/quote_list.html", {"quotes": quotes})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    author_quote_counts = (
        Quote.objects.filter(author_id=author_id)
        .values("author")
        .annotate(count=Count("id"))
    )
    if author_quote_counts:
        author_quots = author_quote_counts[0]["count"]
    else:
        author_quots = 0
    return render(
        request,
        "quotes/author_detail.html",
        {"author": author, "author_quote_counts": author_quots},
    )


def author_quotes(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    quotes = Quote.objects.filter(author=author)
    for quote in quotes:
        print(quote.text)
    return render(
        request, "quotes/author_quotes.html", {"author": author, "quotes": quotes}
    )


@login_required
def upload_file(request, upload_function, template_name):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            data = json.load(file)
            user = request.user
            admin_user = User.objects.filter(is_superuser=True).first()
            upload_function(data, user, admin_user)
            return redirect("quotes:success")
    else:
        form = UploadFileForm()
    return render(request, template_name, {"form": form})


def handle_uploaded_file_authors(data, user, admin_user):
    for item in data:
        born_date = parser.parse(item["born_date"]).date()  # Convert data
        author, created = Author.objects.get_or_create(
            fullname=item["fullname"],
            defaults={
                "born_date": born_date,
                "born_location": item["born_location"],
                "description": item.get("description", ""),
                "added_by": user if user.is_superuser else admin_user,
            },
        )
        if created:
            print(f"Successfully added {author.fullname}")
        else:
            print(f"{author.fullname} already exists")


def success(request):
    return render(request, "quotes/success.html")


def handle_uploaded_file_quotes(data, user, admin_user):
    for item in data:
        # Get or create tags
        tag_objects = []
        for tag_name in item["tags"]:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={"added_by": user if user.is_superuser else admin_user},
            )
            tag_objects.append(tag)

        # Get aythors
        try:
            author = Author.objects.get(fullname=item["author"])
        except Author.DoesNotExist:
            print(f'Author {item["author"]} does not exist')
            continue

        # Create quote
        quote, created = Quote.objects.get_or_create(
            text=item["quote"],
            author=author,
            defaults={"added_by": user if user.is_superuser else admin_user},
        )

        # Add tags to quote
        if created:
            quote.tags.add(*tag_objects)
            print(f"Successfully added quote: {quote.text}")
        else:
            print(f"Quote already exists: {quote.text}")


def upload_file_authors(request):
    return upload_file(
        request, handle_uploaded_file_authors, "quotes/upload_authors.html"
    )


def upload_file_quotes(request):
    return upload_file(
        request, handle_uploaded_file_quotes, "quotes/upload_quotes.html"
    )
