from django import forms
from .models import Post


class PostModelForm(forms.ModelForm):
    '''title2 = forms.CharField(
        max_length=120,
        label='Some field',
        help_text='some help text',
        error_messages={
            'required': 'Title filed is required'
        })'''

    class Meta:
        model = Post
        fields = ['user','title','slug']
        #exclude = []

        labels = {
            'title': 'This is title'
        }
        help_text = {
            'title': 'Title help text'
        }
        error_messages = {
            'title': {
                'max_length': 'This is too long',
                'required': 'Title is required!!!'
            }
        }

    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = forms.Textarea()
        #override Meta error_messages
        self.fields['title'].error_messages = {
            'required': 'Title rquired in __init__'
        }


    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        return title

    def save(self, commit=True, *args, **kwargs):
        obj = super(PostModelForm, self).save(commit=False, *args, **kwargs)
        obj.title = 'T'
        obj.publish ="2018-01-01"
        if commit:
            obj.save()
        return obj


CHOICE = (
    ('db-value', 'Display'),
    ('db-value2', 'Display 2'),
)

INTS_CHOICE = [(x,x) for x in range(0,10)]

class SearchForm(forms.Form):
    year = forms.DateField(widget=forms.SelectDateWidget(years=[2000,3000]))
    search = forms.CharField(label='search label', widget=forms.Textarea(attrs={'rows':3}))
    choice = forms.CharField(label='search label', widget=forms.Select(choices=CHOICE))
    boolean = forms.BooleanField(label='')
    email = forms.EmailField()
    number = forms.IntegerField(initial=9, widget=forms.Select(choices=INTS_CHOICE))

    def clean_number(self):
        '''only run if the valid clean data check finished'''
        number = self.cleaned_data.get('number')
        if number < 5:
            raise forms.ValidationError('Int must greater than 10')
        #return the field value
        return number



