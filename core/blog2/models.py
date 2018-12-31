from datetime import timedelta, datetime, date

from django.db import models
from django.utils.encoding import smart_text
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timesince import timesince, timeuntil

from django.db.models.signals import post_save, pre_save

from .validators import validate_author_email

PUBLISH_CHOICES = (
    ('draft', 'Draft'),
    ('publish', 'Publish'),
    ('private', 'Private'),
)

#Override QuerySet
'''Extend the Modal Manager with custom predefined queries
'''
class PostModelQuerySet(models.query.QuerySet):
   def post_title_items(self, value):
       return self.filter(title__icontains=value)

   def active(self):
       return self.filter(active=True)

#override Model Manager
class PostModelManager(models.Manager):
    def get_queryset(self):
        #return super().get_queryset().filter(active=True)
        return PostModelQuerySet(self.model, using=self._db)

    #override: to be safe *args, **kwargs
    def all(self, *args, **kwargs):
        #qs = super(PostModelManager, self).all(*args, **kwargs)
        qs = self.get_queryset().active()
        return qs

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    title = models.CharField(
        max_length=50,
        verbose_name='Post Title',
        unique=True,
        error_messages={
            'unique': 'This title is not unique'
        },
        help_text='Must be a unique title'
    )
    content = models.TextField(null=True, blank=True)
    publish = models.CharField(max_length=120, choices=PUBLISH_CHOICES, default='draft')
    view_count = models.IntegerField(default=0)
    publish_date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    author_email = models.CharField(validators=[validate_author_email], max_length=240, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # The default manager.
    #New Model Manager for active only
    objects_active = PostModelManager()

    class Meta:
        verbose_name = 'Post Long name'
        verbose_name_plural = 'Posts'
        #unique_together = [('title', 'slug')]

    def __str__(self):
        return smart_text(self.title)

    @property
    def age(self):
        now = timezone.now()
        publish_time = datetime.combine(
            self.publish_date,
            datetime.now().min.time()
        )
        try:
            difference = now - publish_time
        except:
            return "Not published"
        if difference <= timedelta(minutes=1):
            return 'just now'

        return '{time} ago'.format(time=timesince(publish_time).split(', ')[0])

    def save(self, *args, **kwargs):
        #if not self.slug:
            #self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


def post_model_pre_save_reciver(sender, instance, *args, **kwargs):
    if not instance.slug and instance.title:
        instance.slug = slugify(instance.title)

pre_save.connect(post_model_pre_save_reciver, sender=Post)

def post_model_post_save_reciver(sender, instance, created, *args, **kwargs):
    if not instance.slug and instance.title:
        instance.slug = slugify(instance.title)
        instance.save()

post_save.connect(post_model_post_save_reciver, sender=Post)