from django.shortcuts import render
from .forms import SearchForm, PostModelForm

from django.forms import formset_factory, modelformset_factory
from django.utils import timezone

from .models import Post

def home(request):
    form = PostModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.publish = '2010-10-10'
        obj.title = 'Some Random Title'
        obj.save()
    if form.has_error:
        print(form.errors.as_json())

    '''form = SearchForm(request.POST or None, initial={'search': request.user})
    if form.is_valid():
        print(form.cleaned_data)'''

    return render(request, 'htmlforms/form.html', {'abc': form})

def formsets(request):
    '''TestFromset = formset_factory(SearchForm, extra=2)
    formset = TestFromset(request.POST or None)
    if formset.is_valid():
        for form in formset:
            print(form.cleaned_data)
    context = {
        'formset': formset
    }
    return render(request, 'htmlforms/formsets.html', context)
    '''
    #Modelformset
    PostFromset = modelformset_factory(Post, form=PostModelForm)
    formset = PostFromset(request.POST or None, queryset=Post.objects.filter(id__gt=5))
    if formset.is_valid():
        for form in formset:
            obj = form.save(commit=False)
            obj.publish = '2018-10-10'
            obj.save()
    context = {'formset': formset}
    return render(request, 'htmlforms/formsets.html', context)
