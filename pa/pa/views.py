# pa/views.py
from django.shortcuts import render


def random_quote_api(request):
    return render(request, "quotes/random_quote_api.html")

def handler404(request, exception):
    return render(request, 'quotes/404.html', status=404)


