from django.conf.urls import url
from locations import views

urlpatterns = [
    url(r'^$',views.index),
]