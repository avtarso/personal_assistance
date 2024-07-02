from django.conf.urls import handler404
from pa.views.error_views import handler404  # импортируйте ваш обработчик

handler404 = 'pa.views.error_views.handler404'