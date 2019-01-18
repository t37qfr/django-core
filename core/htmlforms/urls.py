from django.conf.urls import url

from .views import home, formsets

#Required for namespaces
app_name = 'htmlforms'

urlpatterns = [
    url(r'^formsets/$', formsets, name='formsets'),
    url(r'^$', home, name='home'),
]
