from django.contrib import admin

from .models import School, Mandal, District, SchoolCategory
# Register your models here.

admin.site.register(District)
admin.site.register(Mandal)
admin.site.register(School)
admin.site.register(SchoolCategory)
