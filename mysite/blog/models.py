from django.db import models
from django.utils import timezone # for time
from django.contrib.auth.models import User # for user authentication



# manager to extract posts
class PublishedManager(models.Manager):
    def get_queryset(self):

        return super().get_queryset() \
            .filter(status=Post.Status.PUBLISHED)

# model for posts of blog
class Post(models.Model):

    # status of posts (draft or published)
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField(max_length=250) # field of Title of posts, in base
    slug = models.SlugField(max_length=250)
    body = models.TextField() # field of Body of posts
    publish = models.DateTimeField(default=timezone.now) # field, publish time of post in the DATETIME colomn
    created = models.DateTimeField(auto_now_add=True) # field, creating time of pos
    updated = models.DateTimeField(auto_now=True) # field, time or edit post
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT) # concern of status of post (draft, publish)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')


    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер

    class Meta:
        ordering = ['-publish'] # Django sorts post by date
        indexes = [
            models.Index(fields=['-publish']), # indexing
        ]


    def __str__(self):
        return self.title