from django.conf.urls import url,include
from django.contrib import admin
from locations import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='home'),
    url(r'^locations/', include('locations.urls'), name='locations'),
]
