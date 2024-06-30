# storage/views.py
import requests
import logging
import datetime

from django.conf import settings
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404
from django.views.generic import ListView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import FileUploadForm, FileTagForm, UploadedFileEditForm, FileFindForm
from .models import UploadedFile, FileTag


logger = logging.getLogger(__name__)

form_search = FileFindForm()

def paginate_data(request, data):
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
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_name = file.name
            # Send File to Telegram
            telegram_bot_token = settings.TELEGRAM_TOKEN
            chat_id = settings.TELEGRAM_CHAT
            response = requests.post(
                f'https://api.telegram.org/bot{telegram_bot_token}/sendDocument',
                data={'chat_id': chat_id},
                files={'document': file}
            )
            if response.status_code == 200:
                telegram_file_id = response.json()['result']['document']['file_id']
                file_size = response.json()['result']['document']['file_size']
                tg_message_id = response.json()['result']['message_id']
                uploaded_file_instance = form.save(commit=False)
                uploaded_file_instance.user = request.user
                uploaded_file_instance.file_name = file_name
                uploaded_file_instance.telegram_file_id = telegram_file_id
                uploaded_file_instance.file_size = file_size
                uploaded_file_instance.tg_message_id = tg_message_id
                uploaded_file_instance.save()
                form.save_m2m()
                return redirect('storage:detail_file', file_id=uploaded_file_instance.id)
            else:
                # Extract error details
                try:
                    error_details = response.json().get('description', 'No details provided')
                except ValueError:  # In case response is not JSON
                    error_details = response.content.decode() if response.content else 'No content provided'
                error_message = f'Failed to upload file to Telegram. Error: {error_details}'
                return render(request, 'storage/upload.html', {'form': form, 'error': error_message, 'form_search': form_search})
    else:
        form = FileUploadForm()
    return render(request, 'storage/upload.html', {'form': form, 'max_file_size': settings.MAX_FILE_SIZE/1024/1024, 'form_search': form_search})


@login_required
def file_list(request):
    files = UploadedFile.objects.filter(user_id=request.user.id).order_by('-upload_time')
    return render(request, "storage/list_file.html", {"files": paginate_data(request, files), "today": datetime.date.today(), 'form_search': form_search})


@login_required
def download_file(request, file_id):
    try:
        uploaded_file = get_object_or_404(UploadedFile, id=file_id)
        telegram_file_id = uploaded_file.telegram_file_id
        tg_token = settings.TELEGRAM_TOKEN
        tg_file_info_url = f'https://api.telegram.org/bot{tg_token}/getFile?file_id={telegram_file_id}'
        response = requests.get(tg_file_info_url)
        response.raise_for_status()
        file_path = response.json()['result']['file_path']
        download_url = f'https://api.telegram.org/file/bot{tg_token}/{file_path}'
        tg_response = requests.get(download_url)
        tg_response.raise_for_status()
        response = HttpResponse(tg_response.content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file_name}"'
        response['Content-Length'] = uploaded_file.file_size
        return response

    except requests.exceptions.RequestException as e:
        logger.error(f"Error request to Telegram Bot API:: {str(e)}")
        raise Http404("Error when requesting file information")
    except KeyError as e:
        logger.error(f"Error extracting data from JSON response: {str(e)}")
        raise Http404("Error when processing data from Telegram")
    except Exception as e:
        logger.exception("An error occurred while downloading the file")
        raise Http404("An error occurred while downloading the file")


@login_required
def delete_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    return render(request, 'storage/delete_file_confirm.html', {'file': uploaded_file, 'form_search': form_search})


@login_required
def delete_file_confirmed(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    telegram_bot_token = settings.TELEGRAM_TOKEN
    chat_id = settings.TELEGRAM_CHAT
    response = requests.post(f'https://api.telegram.org/bot{telegram_bot_token}/deleteMessage',
        data={'chat_id': chat_id, 'message_id': uploaded_file.tg_message_id},)
    uploaded_file.delete()
    return redirect('storage:file_list')


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = FileTagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.added_by = request.user
            tag.save()
            return redirect("storage:tag_list")
    else:
        form = FileTagForm()
    return render(request, "storage/add_tag.html", {"form": form, "form_search": form_search})


@login_required
def tag_list(request):
    tags = FileTag.objects.filter(added_by=request.user).annotate(
        num_files=Count('uploadedfile')).order_by('name')
    
    without_tags = UploadedFile.objects.filter(user=request.user,
        tags__isnull=True).count()
    
    return render(request, 'storage/list_tag.html', {'tags': tags, 'without_tags': without_tags, 'form_search': form_search})


@login_required
def delete_tag(request, tag_id):
    tag = get_object_or_404(FileTag, id=tag_id)
    return render(request, 'storage/delete_tag_confirm.html', {'tag': tag, 'form_search': form_search})


@login_required
def delete_tag_confirmed(request, tag_id):
    tag = get_object_or_404(FileTag, id=tag_id)
    tag.delete()
    return redirect('storage:tag_list')


@login_required
def tag(request, tag_id):
    tag = get_object_or_404(FileTag, added_by=request.user.id, id=tag_id)
    files = get_list_or_404(UploadedFile, user=request.user.id, tags__id=tag_id)
    return render(request, 'storage/list_file_tag.html', {'tag': tag, 'files': paginate_data(request, files), "today": datetime.date.today(), 'form_search': form_search})


@login_required
def tag_none(request):
    files = get_list_or_404(UploadedFile, user=request.user.id, tags__isnull=True)
    return render(request, 'storage/list_file_tag.html', {'files': paginate_data(request, files), "today": datetime.date.today(), 'form_search': form_search})


@login_required
def edit_tag(request, tag_id):
    tag = get_object_or_404(FileTag, id=tag_id)
    if request.method == 'POST':
        form = FileTagForm(request.POST, instance=tag)
        form.save()
        return redirect('storage:tag', tag_id)
    else:
        form = FileTagForm(instance=tag)
    return render(request, 'storage/edit_tag.html', {'form': form, 'tag': tag, 'form_search': form_search})


@login_required
def edit_file(request, file_id):
    edited_file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    if request.method == 'POST':
        form = UploadedFileEditForm(request.POST, instance=edited_file)
        if form.is_valid():
            form.save()
            return redirect('storage:detail_file', file_id=edited_file.id)
    else:
        form = UploadedFileEditForm(instance=edited_file)
    return render(request, 'storage/edit_file.html', {'form': form, 'file': edited_file, 'form_search': form_search})


@login_required
def detail_file(request, file_id):
    detailed_file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    return render(request, 'storage/detail_file.html', {'file': detailed_file, "today": datetime.date.today(), 'form_search': form_search})


@login_required
def find_file(request):
    find_text = ""
    form = FileFindForm(request.POST or None)
    files = UploadedFile.objects.none()
    if request.method == 'POST' and form.is_valid():
        find_text = form.cleaned_data['find_text'].strip()
        if find_text:
            files = UploadedFile.objects.filter(
        Q(description__icontains=find_text) | Q(file_name__icontains=find_text)).order_by('-upload_time')
    return render(request, "storage/find_file.html", {"form": form, "files": paginate_data(request, files), "find_text": find_text, "today": datetime.date.today(), 'form_search': form_search})


@login_required
def file_list_upcoming_date(request):
    files = UploadedFile.objects.filter(user_id=request.user.id
            ).exclude(attention_date__isnull=True).order_by('attention_date')
    return render(request, "storage/list_file_upcoming_date.html", {"files": paginate_data(request, files), "today": datetime.date.today(), 'form_search': form_search})


