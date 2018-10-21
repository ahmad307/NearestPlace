from django.conf.urls import url,include
from django.contrib import admin
from locations import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^locations/', include('locations.urls'), name='locations'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
