from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q

from .models import PostModel

from .forms import PostModelForm

def post_model_delete_view(request, id=None):
    obj = get_object_or_404(PostModel, id=id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Delete Success')
        return HttpResponseRedirect('/blog/')

    template = 'blog/delete-view.html'
    context = {
        'obj': obj
    }
    return render(request, template, context)

def post_model_update_view(request, id=None):
    obj = get_object_or_404(PostModel, id=id)
    form = PostModelForm(request.POST or None, instance=obj)

    context = {
        'form': form
    }

    if form.is_valid():
        #because it is a modal form
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, 'Updated Blog Post')
        return HttpResponseRedirect('/blog/{num}'.format(num=obj.id))

    template = 'blog/update-view.html'

    return render(request, template, context)

def post_model_create_view(request):
    form = PostModelForm(request.POST or None)

    context = {
        'form': form
    }

    if form.is_valid():
        #because it is a modal form
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, 'New Blog Post Created')
        context = {
            'form': PostModelForm()
        }
        #return HttpResponseRedirect('/blog/{num}'.format(num=obj.id))

    template = 'blog/create-view.html'

    return render(request, template, context)

def post_model_detail_view(request, id=None):
    obj = get_object_or_404(PostModel, id=id)
    template = 'blog/detail-view.html'
    context = {
        'obj': obj
    }
    return render(request, template, context)

#@login_required
def post_model_list_view(request):
    query = request.GET.get('q', None)
    qs = PostModel.objects.all()
    if query is not None:
       qs = qs.filter(
           Q(title__icontains=query) |
           Q(content__icontains=query) |
           Q(slug__icontains=query)
       )
    template = 'blog/list-view.html'
    context = {
        'qs': qs
    }
    return render(request, template, context)


