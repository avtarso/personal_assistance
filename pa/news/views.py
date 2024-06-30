# from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.defaults import page_not_found

from get_news.spiders.get_news_quotes import GetNewsQuotesSpider
from get_news.spiders.get_news_economics import GetNewsEconomicsSpider
from get_news.spiders.get_news_politics import GetNewsPoliticsSpider
from get_news.spiders.get_news_weather_by_city import GetNewsWeatherByCitySpider

from get_news.main import run_get_news_spider
from news.models import (
    NewsQuote,
    NewsEconomics,
    NewsPolitics,
    NewsWeatherByCity,
    # NewsUpdateTime,
)


def get_request_user_id(request):
    user = User.objects.filter(username=request.user).get()
    return user.id


# def get_news_last_update_time(request, news_type):
#     try:
#         update_time_item = NewsUpdateTime.objects.filter(
#             added_by=request.user, news_type=news_type
#         ).get()

#         last_update_time = update_time_item.update_time.strftime("%d/%m/%Y %H:%M:%S")
#     except:
#         last_update_time = "Never"

#     return last_update_time


# def set_news_last_update_time(request, news_type):
#     try:
#         update_time_item = NewsUpdateTime.objects.filter(
#             added_by=request.user, news_type=news_type
#         ).get()

#         update_time_item.update_time = timezone.now()
#     except:
#         update_time_item = NewsUpdateTime.objects.create(
#             news_type=news_type,
#             update_time=timezone.now(),
#             added_by_id=get_request_user_id(request),
#         )
#     finally:
#         update_time_item.save()


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


@login_required
def main(request):
    per_page = request.GET.get("per_page", 10)
    item_per_page = request.POST.get("item_per_page", None)

    if item_per_page:
        per_page = item_per_page

    news = NewsQuote.objects.filter(added_by=request.user).order_by("id")
    # last_update_time = get_news_last_update_time(request, "quotes")

    return paginations(
        request,
        news,
        per_page,
        "news/news.html",
        {
            "per_page": per_page,
            # "last_update_time": last_update_time,
            "h2": "Quotes",
            "news_type": "quotes",
        },
    )


@login_required
def quotes_get(request):
    if items := NewsQuote.objects.filter(added_by=request.user):
        items.delete()

    uid = get_request_user_id(request)

    run_get_news_spider(GetNewsQuotesSpider, uid)

    # set_news_last_update_time(request, "quotes")

    return redirect(to="news:main")


@login_required
def economics(request):
    per_page = request.GET.get("per_page", 10)
    item_per_page = request.POST.get("item_per_page", None)

    if item_per_page:
        per_page = item_per_page

    news = NewsEconomics.objects.filter(added_by=request.user).order_by("id")
    # last_update_time = get_news_last_update_time(request, "economics")

    return paginations(
        request,
        news,
        per_page,
        "news/news.html",
        {
            "per_page": per_page,
            # "last_update_time": last_update_time,
            "h2": "Economic News",
            "news_type": "economics",
        },
    )


@login_required
def economics_get(request):
    if items := NewsEconomics.objects.filter(added_by=request.user):
        items.delete()

    uid = get_request_user_id(request)

    run_get_news_spider(GetNewsEconomicsSpider, uid)

    # set_news_last_update_time(request, "economics")

    return redirect(to="news:economics")


@login_required
def politics(request):
    per_page = request.GET.get("per_page", 10)
    item_per_page = request.POST.get("item_per_page", None)

    if item_per_page:
        per_page = item_per_page

    news = NewsPolitics.objects.filter(added_by=request.user).order_by("id")
    # last_update_time = get_news_last_update_time(request, "politics")

    return paginations(
        request,
        news,
        per_page,
        "news/news.html",
        {
            "per_page": per_page,
            # "last_update_time": last_update_time,
            "h2": "Political News",
            "news_type": "politics",
        },
    )


@login_required
def politics_get(request):
    if items := NewsPolitics.objects.filter(added_by=request.user):
        items.delete()

    uid = get_request_user_id(request)

    run_get_news_spider(GetNewsPoliticsSpider, uid)

    # set_news_last_update_time(request, "politics")

    return redirect(to="news:politics")


@login_required
def weather(request):
    per_page = "all"
    show_items_per_page = False

    news = NewsWeatherByCity.objects.filter(added_by=request.user).order_by("id")
    # last_update_time = get_news_last_update_time(request, "weather")

    return paginations(
        request,
        news,
        per_page,
        "news/news.html",
        {
            "per_page": per_page,
            "show_items_per_page": show_items_per_page,
            # "last_update_time": last_update_time,
            "h2": "Weather",
            "news_type": "weather",
        },
    )


@login_required
def weather_get(request):
    if items := NewsWeatherByCity.objects.filter(added_by=request.user):
        items.delete()

    uid = get_request_user_id(request)

    run_get_news_spider(GetNewsWeatherByCitySpider, uid)

    # set_news_last_update_time(request, "weather")

    return redirect(to="news:weather")
