from django.conf.urls import url
from locations import views

app_name = 'locations'

urlpatterns = [
    url(r'^get_location', views.get_location),
    url(r'^create_session', views.create_session),
    url(r'^add_location', views.add_location)
]
