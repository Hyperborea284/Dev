from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


User = settings.AUTH_USER_MODEL

class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)

    def search(self, query):

        lookup = (
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(slug__icontains=query)
            )

        return self.filter(lookup)

class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)


class BlogPost(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='image/uploads/', blank=True, null=True)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    content = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    barplot = models.ImageField(upload_to='image/plots/barplots/', blank=True, null=True)
    wordcloud = models.ImageField(upload_to='image/plots/wordclouds/', blank=True, null=True)
    maltego_csv = models.FileField(upload_to='image/plots/maltego_csv/', blank=True, null=True)
    pdfs = models.FileField(upload_to='image/plots/out_pdf/', blank=True, null=True)
    sents_1 = models.FileField(upload_to='image/plots/sents_1/', blank=True, null=True)

    reinert = models.FileField(upload_to='image/plots/reinerts/', blank=True, null=True)

    summ_bert = models.TextField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    article = models.URLField(null=True, blank=True)
    rainette_explor = models.URLField(null=True, blank=True)

    #sents_2 = models.FileField(upload_to='image/plots/sents_2/', blank=True, null=True)


    # associations =
    # entities = 

    objects = BlogPostManager()

    class Meta:
        ordering = ['-pk', '-publish_date', 'updated', '-timestamp'] 


    def get_absolute_url(self):
        return f'/blog/{self.slug}'

    def get_edit_url(self):
        return f'{self.get_absolute_url()}/edit'

    def get_delete_url(self):
        return f'{self.get_absolute_url()}/delete'
