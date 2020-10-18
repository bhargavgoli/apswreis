from django.contrib import admin

from .models import School, Mandal, District, SchoolCategory
# Register your models here


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('district_name', 'created_at',)


class MandalAdmin(admin.ModelAdmin):
    list_display = ('mandal_name', 'district', 'created_at',)


class SchoolCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'point', 'created_at',)


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'address', 'village',
                    'mandal', 'pincode', 'category', 'created_at',)


admin.site.register(District, DistrictAdmin)
admin.site.register(Mandal, MandalAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(SchoolCategory, SchoolCategoryAdmin)
