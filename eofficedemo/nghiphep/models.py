from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
# class PublishedManager(models.Manager):
#     def get_queryset(self):
#         return super(PublishedManager,self).get_queryset().filter(status='published')
class PostQuerySet(models.QuerySet):
    def get_users_posts(self, username):
        return self.filter(author=username)

class PublishedManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)
    def get_users_posts(self, username):
        return self.get_queryset().get_users_posts(username)
# class PublishedManager(models.Manager):
#     def get_queryset(self):
#         return super(PublishedManager,self).get_queryset().filter(status='draft')
STATUS_CHOICES = (('request', 'Request'),('waiting', 'Waiting'),('approved', 'Approved'),('rejected', 'Rejected'),('canceled', 'Canceled'),)
class Post(models.Model):
    TITLE_CHOICES=(('Nghỉ phép', 'Nghỉ phép'),('Nghỉ không lương', 'Nghỉ không lương'),('Nghỉ ốm', 'Nghỉ ốm'),('Nghỉ sanh', 'Nghỉ sanh'),('Nghỉ hôn nhân', 'Nghỉ hôn nhân'),('Nghỉ tang lễ', 'Nghỉ tang lễ'),('Nghỉ khác', 'Nghỉ khác'),)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=100,choices=TITLE_CHOICES,default='Nghỉ phép')
    date_from = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField(default=timezone.now)
    numday = models.FloatField(default=1)
    reason = models.TextField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    approval = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager')
    approvalbod = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='request')
    objects = PostQuerySet.as_manager()
    # published = PublishedManager() # Our custom manager
    def __str__(self):
        return self.title
# 'Profile for user {}'.format(self.user.username)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    