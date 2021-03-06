from django.contrib import admin
from django.conf.urls import url, include

from .views import home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^newsletter/', include('newsletter.urls', namespace='newsletter')),
    url(r'^forms/', include('htmlforms.urls', namespace='form')),
    url(r'^$', home, name='home')
]
