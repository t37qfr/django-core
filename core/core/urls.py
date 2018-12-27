from django.contrib import admin
from django.conf.urls import url

from .views import home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home')
]
