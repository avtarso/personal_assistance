import json

from dateutil import parser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NoteForm
from .models import Note, Tag


@login_required
def note(request, id):
    note = get_object_or_404(Note, id=id, added_by=request.user)
    return render(request, "notes/note.html", {"note": note})


@login_required
def all_notes(request):
    notes = Note.objects.filter(added_by=request.user).order_by("-id")
    return render(request, "notes/all_notes.html", {"notes": notes})


@login_required
def add_note(request):
    if request.method == "POST":

        raw_tags = request.POST.get('tags')
        tags = []
        for t in raw_tags.split(','):
            tag, _ = Tag.objects.get_or_create(name=t.strip())
            tags.append(tag)

        user = request.user
        note_name = request.POST.get('name')
        description = request.POST.get('description')
        note = Note.objects.create(
            name=note_name,
            description=description,
            added_by=user
        )
        note.tags.set(tags)

        return redirect('notes:all_notes')

    return render(request, "notes/add_note.html")


@login_required
def edit_note(request, id):
    note = get_object_or_404(Note, id=id, added_by=request.user)
    if request.method == "POST":
        note.name = request.POST["new_name"]
        note.description = request.POST["new_description"]

        raw_tags = request.POST["new_tags"]
        tags = []
        for t in raw_tags:
            tag, _ = Tag.objects.get_or_create(name=t.strip())
            tags.append(tag)

        note.tags.set(tags)
        note.save()

        return redirect('notes:all_notes')
    return render(request, 'notes/edit_note.html', {'note': note})


@login_required
def delete_note(request, id):
    note = get_object_or_404(Note, id=id, added_by=request.user)
    if request.method == "POST":
        note.delete()
        return redirect('notes:all_notes')
    return render(request, "notes/delete_note.html", {"note": note})


@login_required
def find_notes(request):
    return render(request, "notes/find_notes.html")


@login_required
def by_name(request):
    notes = []
    if request.method == "POST":
        name = request.POST.get("name", "")
        notes = Note.objects.filter(name__icontains=name, added_by=request.user)
    return render(request, "notes/search_result.html", {"notes": notes})


@login_required
def by_tag(request):
    notes = []
    if request.method == "POST":
        tag = request.POST.get("tag", "")
        notes = Note.objects.filter(tags__name__icontains=tag, added_by=request.user)
    return render(request, "notes/search_result.html", {"notes": notes})