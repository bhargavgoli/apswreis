from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


def getChornic(id):
    illness = {
        "0": "Not Applicable",
        "1": "Cancer",
        "2": "Kidney",
        "3": "Thalassemia",
        "4": "Others"
    }
    return illness[id]


class Application(models.Model):
    app_ref_no = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    date_of_join = models.DateField(blank=True, null=True)
    years_of_exp = models.IntegerField(default=0)
    marital_status = models.BooleanField(default=False)
    physical_disabled = models.BooleanField(default=False)
    chronic_illness = models.CharField(default=0, max_length=100)
    gender = models.CharField(max_length=6)
    status = models.CharField(default="Pending", max_length=25)
    points = models.IntegerField(default=0)
    is_submitted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        get_user_model(), related_name='user', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} {}'.format(self.app_ref_no, self.first_name, self.last_name)

    def marital(self):
        return 'Married' if self.marital_status else 'Single'

    def physical_disability(self):
        return 'Yes' if self.physical_disabled else 'No'

    def ChronicIllness(self):
        return getChornic(self.chronic_illness)

    def user_gender(self):
        return 'Male' if self.gender == '1' else 'Female'


class TransferAllotment(models.Model):
    school = models.ForeignKey(
        'masters.School', related_name='school', on_delete=models.DO_NOTHING)
    application = models.ForeignKey(
        'applications.Application', related_name='application', on_delete=models.DO_NOTHING)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
