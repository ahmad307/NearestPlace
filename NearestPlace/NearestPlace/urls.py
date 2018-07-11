from django.conf.urls import url,include
from django.contrib import admin
from locations import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',include('locations.urls')),
    url(r'^get_location',views.get_location),
]
