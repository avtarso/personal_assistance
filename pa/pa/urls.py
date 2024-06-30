"""
URL configuration for pa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from quotes import views as quotes_views
from users import views as user_views
from storage import views as storage_views

from .api import NewsQuoteResource

news_quote_resource = NewsQuoteResource()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", quotes_views.top_10_tag_list, name="main"),
    path("", include("notes.urls")),
    path("", include("contacts.urls")),
    path("users/", include("users.urls")),
    path("quotes/", include("quotes.urls")),
    path("news/", include("news.urls")),
    path("storage/", include("storage.urls")),
    re_path(r"^api/", include(news_quote_resource.urls)),
]
