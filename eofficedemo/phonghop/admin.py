from django.contrib import admin
from .models import LichHop, PhanQuyen, GhichuLichHop
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin
from import_export import resources
# Register your models here.
class LichHopAdmin(admin.ModelAdmin):
    list_display = ['title','author','date', 'time_from','time_end']
    list_filter = ['date']
    search_fields = ['title']
admin.site.register(LichHop, LichHopAdmin)

# class PhanQuyenAdmin(admin.ModelAdmin):
#     list_display = ['category','qlphonghop']
#     list_filter = ['category']
#     search_fields = ['category']
# admin.site.register(PhanQuyen, PhanQuyenAdmin)
admin.site.register(GhichuLichHop)

class PhanQuyenResource(resources.ModelResource):
    class Meta:
        model = PhanQuyen
        fields = ('id','name', 'qlphonghop')
class PhanQuyenAdmin(ImportExportModelAdmin):
    resource_classes = [PhanQuyenResource]
    ordering = ['id']
admin.site.register(PhanQuyen, PhanQuyenAdmin)
