from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
GIOITINH_CHOICES = (('Nam', 'Nam'),('Nữ', 'Nữ'),)
CHUCDANH_CHOICES = (('Tổng giám đốc', 'Tổng giám đốc'),('Phó tổng giám đốc', 'Phó tổng giám đốc'),('Giám đốc dự án', 'Giám đốc dự án'),('Trưởng phòng', 'Trưởng phòng'),('Trưởng ban', 'Trưởng ban'),('Chỉ huy trưởng', 'Chỉ huy trưởng'),('Nhân viên', 'Nhân viên'),)
class Department(models.Model):
    name = models.CharField(max_length=50)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='department')
    bod = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bod')
    gd = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gd')
    def __str__(self):
        return self.name



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    msnv = models.CharField(max_length=10, blank=True)
    hovaten = models.CharField(max_length=50)
    phongban = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True)
    chucdanh = models.CharField(max_length=50,choices=CHUCDANH_CHOICES,default='Nhân viên')
    gioitinh = models.CharField(max_length=10,choices=GIOITINH_CHOICES,default='Nam')
    ngaysinh = models.DateField(blank=True, null=True)
    sophepnam = models.FloatField(blank=True, default=12)
    songaynghiphep = models.FloatField(blank=True, default=0)
    songaynghikhongphep = models.FloatField(blank=True, default=0)
    songaynghiphepconlai = models.FloatField(blank=True, default=12)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',blank=True)
    phone = models.CharField(max_length=15)
    ngayvaocty = models.DateField(blank=True, null=True)
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

