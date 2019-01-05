from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import View
from django.views.generic.base import TemplateView, TemplateResponseMixin, ContextMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Book
from .forms import BookForm


class MultipleObjectMixin(object):
    # overwrite get object
    def get_object(self, queryset=None, *args, **kwargs):
        slug = self.kwargs.get('slug')
        if slug:
            try:
                obj = self.model.objects.get(slug=slug)
            except self.model.MultipleObjectReturned:
                obj = self.get_queryset().first()
            except:
                raise Http404
            return Http404
        return None

class BookDelete(DeleteView):
    model = Book
    template_name = 'newsletter/book_delete.html'

    def get_success_url(self):
        return reverse('newsletter:book_list')

class BookUpdate(MultipleObjectMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'newsletter/book_update.html'

class BookCreate(SuccessMessageMixin, CreateView):
    model = Book

    '''Better because use form validation things'''
    #fields = ['title', 'description']
    form_class = BookForm

    success_message = '%(title)s has been created, %(created_at)s'

    def form_valid(self, form):
        '''Add logged in user info when the form is saved'''
        form.instance.added_by = self.request.user
        form.instance.last_edited_by = self.request.user
        #for messages order count
        valid_form = super(BookCreate, self).form_valid(form)
        # messages.success(self.request, 'Book created')
        return valid_form

    def get_success_url(self):
        return reverse('newsletter:book_list')

    #customize success message as you want
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            created_at = self.object.timestamp,
        )

    template_name = 'newsletter/book_create.html'

class BookList(ListView):
    model = Book
    template_name = 'newsletter/book_list.html'
    context_object_name = 'books'

    #override query set
    def get_queryset(self, *args, **kwargs):
        qs = super(BookList, self).get_queryset(*args, **kwargs).order_by('-timestamp')
        return qs

class BookDetail(MultipleObjectMixin, DetailView):
    model = Book
    template_name = 'newsletter/book_detail.html'
    #rename the basic 'object' name
    context_object_name = 'book'


    # object is the name of the basic context
    '''def get_context_data(self, **kwargs):
        context = super(BookDetail,self).get_context_data(**kwargs)
        return context'''

class DashboardTemplateView(TemplateView):
    template_name = 'newsletter/about.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'This is about us'
        return context


'''Recreation of Login Requirements
    Order is important!
'''
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kw):
        view = super(LoginRequiredMixin, cls).as_view(**kw)
        return login_required(view)

'''TemplateView Recreation from other base elements
'''
class MyView(LoginRequiredMixin, ContextMixin, TemplateResponseMixin, View):
    template_name = 'newsletter/about.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['title'] = 'new title'
        return self.render_to_response(context)
