from django.conf.urls import url
from locations import views

app_name = 'locations'

urlpatterns = [
    url(r'^meeting', views.meeting, name='meeting'),
]
