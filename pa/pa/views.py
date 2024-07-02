# pa/views.py
from django.shortcuts import render


def random_quote_api(request):
    return render(request, "quotes/random_quote_api.html")


