import json

from dateutil import parser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .models import Contact


@login_required
def contacts(request):
    contacts = Contact.objects.filter(added_by=request.user).all()
    return render(request, "contacts/contacts.html", {"contacts": contacts})