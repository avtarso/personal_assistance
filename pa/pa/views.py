# pa/views.py
from django.shortcuts import render


def random_quote_api(request):
    return render(request, "random_quote_api.html")

def handler404(request, exception):
    return render(request, '404.html', status=404)

def main_page(request):
    return render(request, "index.html")

def road_map(request):
    return render(request, "road_map.html")

def reviews(request):
    return render(request, "reviews.html")


