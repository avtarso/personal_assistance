# pa/views.py
from django.shortcuts import render


def random_quote_api(request):
    return render(request, "random_quote_api.html")

def handler404(request, exception):
    return render(request, '404.html', status=404)

def main_page(request):
    return render(request, "index.html")


