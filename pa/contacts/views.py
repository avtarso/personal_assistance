from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Contact
from .forms import ContactForm


@login_required
def contact(request, id):
    contact = get_object_or_404(Contact, id=id, added_by=request.user)
    return render(request, "contacts/contact.html", {"contact": contact})


@login_required
def contacts(request):
    contacts = Contact.objects.filter(added_by=request.user).all()
    return render(request, "contacts/contacts.html", {"contacts": contacts})


@login_required
def create_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            contact.added_by = request.user
            contact.save()
            return redirect("contacts:contacts")
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
            return redirect("contacts:contacts")
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
        result = Contact.objects.filter(name__icontains=search_word, added_by=request.user)
        if not result.exists():
            result = Contact.objects.filter(email__icontains=search_word, added_by=request.user)
        if not result.exists():
            result = Contact.objects.filter(phone__icontains=search_word, added_by=request.user)
    return render(request, "contacts/search_result.html", {"contacts": result})



