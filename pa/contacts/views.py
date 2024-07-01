from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from .models import Contact
from .forms import ContactForm


def paginator(request, data):
    paginator = Paginator(data, 5)  # Number elements on page
    page = request.GET.get('page', 1)
    try:
        data_paginated = paginator.page(page)
    except PageNotAnInteger:
        data_paginated = paginator.page(1)
    except EmptyPage:
        data_paginated = paginator.page(paginator.num_pages)
    return data_paginated


@login_required
def contact(request, id):
    contact = get_object_or_404(Contact, id=id, added_by=request.user)
    return render(request, "contacts/contact.html", {"contact": contact})


@login_required
def contacts(request):
    contacts = Contact.objects.filter(added_by=request.user).all().order_by('name')
    return render(
        request,
        "contacts/contacts.html",
        {
            "contacts": paginator(request, contacts)
        }
    )


@login_required
def create_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            contact.added_by = request.user
            contact.save()
            return redirect("contacts:contact", contact.id)
        else:
            return render(request, "contacts/create_contact.html", {"form": form})
    return render(request, "contacts/create_contact.html", {"form": ContactForm()})


@login_required
def edit_contact(request, id):
    contact = get_object_or_404(Contact, id=id, added_by=request.user)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect("contacts:contact", id)
    else:
        form = ContactForm(instance=contact)

    return render(request, "contacts/edit_contact.html", {"form": form, "contact": contact})


@login_required
def delete_contact(request, id):
    contact = get_object_or_404(Contact, id=id, added_by=request.user)
    if request.method == "POST":
        contact.delete()
        return redirect("contacts:contacts")
    return render(request, "contacts/delete_contact.html", {"contact": contact})


@login_required
def find_contact(request):
    result = []
    if request.method == "POST":
        search_word = request.POST.get("search_word", "")
        result = Contact.objects.filter(name__icontains=search_word, added_by=request.user).order_by('name')
        if not result.exists():
            result = Contact.objects.filter(email__icontains=search_word, added_by=request.user).order_by('name')
        if not result.exists():
            result = Contact.objects.filter(phone__icontains=search_word, added_by=request.user).order_by('name')
    return render(
        request,
        "contacts/search_result.html",
        {
            "contacts": paginator(request, result)
        }
    )


@login_required
def upcoming_birthdays(request):
    today = date.today()
    end_date = today + timedelta(days=7)

    upcoming_birthdays = Contact.objects.filter(
        added_by=request.user,
        birthday__isnull=False,
        birthday__month__in=[today.month, end_date.month],
        birthday__day__gte=today.day if today.month == end_date.month else 1,
        birthday__day__lte=end_date.day if today.month == end_date.month else 31
    ).order_by('-birthday')
    return render(
        request,
        "contacts/contacts.html",
        {
            "contacts": paginator(request, upcoming_birthdays)
        }
    )
