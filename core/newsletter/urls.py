from django.conf.urls import url

from .views import DashboardTemplateView, MyView, BookDetail,BookList, BookCreate, BookUpdate, BookDelete


#Required for namespaces
app_name = 'newsletter'

urlpatterns = [
    url(r'^about/$', DashboardTemplateView.as_view(), name='about'),
    url(r'^myview/$', MyView.as_view(), name='myview'),
    url(r'^book/$', BookList.as_view(), name='book_list'),
    url(r'^book/create/$', BookCreate.as_view(), name='book_create'),
    url(r'^book/(?P<slug>[-\w]+)/update/$', BookUpdate.as_view(), name='book_update'),
url(r'^book/(?P<slug>[-\w]+)/delete/$', BookDelete.as_view(), name='book_delete'),
    url(r'^book/(?P<slug>[-\w]+)/$', BookDetail.as_view(), name='book_detail'),

]
