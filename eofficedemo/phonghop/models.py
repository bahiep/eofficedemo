from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
STATUS_CHOICES = (('request', 'Request'),('waiting', 'Waiting'),('approved', 'Approved'),('rejected', 'Rejected'),('canceled', 'Canceled'),)
ROOM_CHOICES = (('OPAL', 'OPAL'),('RUBY', 'RUBY'),('AMBER', 'AMBER'),('SAPHIRE', 'SAPHIRE'),('DIAMOND', 'DIAMOND'),)
KIND_CHOICES = (('Online', 'Online'),('Offline', 'Offline'),('Online và Offline', 'Online và Offline'),)

class LichHop(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='phonghop')
    title=models.CharField(max_length=50)
    date=models.DateField()
    time_from=models.TimeField()
    time_end=models.TimeField()
    num_per=models.IntegerField()
    room=models.CharField(max_length=15,choices=ROOM_CHOICES,default='RUBY')
    kind = models.CharField(max_length=50,choices=KIND_CHOICES,default='Offline')
    approval = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hcns')
    status = models.CharField(max_length=15,choices=STATUS_CHOICES,default='request')
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class GhichuLichHop(models.Model):
    post = models.ForeignKey(LichHop, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

class PhanQuyen(models.Model):
    category = models.CharField(max_length=50)
    qlphonghop = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qlphonghop')
    qlnhansu = models.ManyToManyField(User, related_name='qlnhansu', default=None, blank=True)