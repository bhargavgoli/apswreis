from django.contrib import admin
from .models import Application, TransferAllotment
# Register your models here.


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('app_ref_no', 'first_name', 'last_name', 'email', 'employee_id',
                    'phone_no', 'date_of_join', 'years_of_exp', 'marital',
                    'physical_disability', 'ChronicIllness', 'user_gender', 'status', 'points', 'is_submitted', 'created_at')


class TransferAllotmentAdmin(admin.ModelAdmin):
    list_display = ('application', 'school', 'points')


admin.site.register(Application, ApplicationAdmin)
admin.site.register(TransferAllotment, TransferAllotmentAdmin)
