from django.conf.urls import url,include
from django.contrib import admin
from locations import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^locations/', include('locations.urls'), name='locations'),
    url(r'^get_location', views.get_location),
    url(r'^create_session', views.create_session),
    url(r'^admin/', admin.site.urls),
]
