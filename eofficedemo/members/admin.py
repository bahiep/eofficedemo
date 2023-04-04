from django.contrib import admin
from .models import Department, Profile
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin
from import_export import resources
# Register your models here.

class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department
        fields = ('id','name', 'manager', 'bod','gd')
class DepartmentAdmin(ImportExportModelAdmin):
    resource_classes = [DepartmentResource]
    ordering = ['id']
admin.site.register(Department, DepartmentAdmin)

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile
        # fields = ('user_id', 'msnv', 'hovaten','phongban','chucdanh','gioitinh','ngaysinh','photo','ngayvaocty')
        fields = ('id','user', 'msnv', 'hovaten','phongban','chucdanh','gioitinh','sophepnam','songaynghiphep','songaynghikhongphep','songaynghiphepconlai','ngaysinh','photo','ngayvaocty','phone')
        # fields = '__all__'
class ProfileAdmin(ImportExportModelAdmin):
    resource_classes = [ProfileResource]
    list_display = ['user','hovaten', 'ngayvaocty']
    # import_id_fields = ['id']
    ordering = ['id']
admin.site.register(Profile, ProfileAdmin)
# admin.site.register(Profile)

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_login','is_superuser','first_name','last_name','email','password','is_staff','is_active','date_joind')
        # fields = ('id','username', 'first_name', 'last_name','email')
class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    # import_id_fields = ['id']
    ordering = ['id']
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

