from django.contrib import admin

# Register your models here.
from .models import Post


class PostAdmin(admin.ModelAdmin):
    fields = ('active','title','slug','updated','get_age')

    readonly_fields = ['updated', 'timestamp', 'get_age']

    list_display = ['title', 'active']

    def get_age(self, obj):
        '''Calculated custom fields has to be readonly_fields as well'''
        return obj.age

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)