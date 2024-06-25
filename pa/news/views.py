from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.defaults import page_not_found

from get_news.main import (
    run_get_news_quotes_spider,
    run_get_news_economics_spider,
    run_get_news_politics_spider,
)
from news.models import NewsQuote, NewsEconomics, NewsPolitics


def paginations(request, data, item_on_page: int | str, template: str, other_data={}):
    page_number = request.GET.get("page", 1)

    if page_number == "all" or item_on_page == "all" or not data:
        return render(
            request,
            template,
            {"show_all_pages": True, "show_items_per_page": True, "page_obj": data}
            | other_data,
        )

    paginator = Paginator(data, item_on_page)

    try:
        page_number = int(page_number)
    except:
        return page_not_found(request, "404", "news/404.html")

    if page_number > paginator.count:
        return page_not_found(request, "404", "news/404.html")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        template,
        {"show_all_pages": False, "page_obj": page_obj} | other_data,
    )


def main(request):

    per_page = request.GET.get("per_page", 10)
    item_per_page = request.POST.get("item_per_page", None)

    if item_per_page:
        per_page = item_per_page

    news = NewsQuote.objects.all()

    return paginations(
        request,
        news,
        per_page,
        "news/news.html",
        {"per_page": per_page, "h2": "Цитати відомих людей", "news_type": "quotes"},
    )


def quotes_get(request):
    if items := NewsQuote.objects.all():
        items.delete()
    run_get_news_quotes_spider()
    return redirect(to="news:main")


def economics(request):
    per_page = request.GET.get("per_page", 10)
    item_per_page = request.POST.get("item_per_page", None)

    if item_per_page:
        per_page = item_per_page

    news = NewsEconomics.objects.all()

    return paginations(
        request,
        news,
        per_page,
        "news/news.html",
        {"per_page": per_page, "h2": "Економічні новини", "news_type": "economics"},
    )


def economics_get(request):
    if items := NewsEconomics.objects.all():
        items.delete()
    run_get_news_economics_spider()
    return redirect(to="news:economics")


def politics(request):
    per_page = request.GET.get("per_page", 10)
    item_per_page = request.POST.get("item_per_page", None)

    if item_per_page:
        per_page = item_per_page

    news = NewsPolitics.objects.all()

    return paginations(
        request,
        news,
        per_page,
        "news/news.html",
        {"per_page": per_page, "h2": "Політичні новини", "news_type": "politics"},
    )


def politics_get(request):
    if items := NewsPolitics.objects.all():
        items.delete()
    run_get_news_politics_spider()
    return redirect(to="news:politics")


def weather_forecast(request):
    pass


def weather_forecast_get(request):
    pass
