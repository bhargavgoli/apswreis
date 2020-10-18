from django.db import models
import datetime
from django.utils import timezone

# Create your models here.


class District(models.Model):
    district_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.district_name


class Mandal(models.Model):
    district = models.ForeignKey(
        'masters.District', related_name='district', on_delete=models.DO_NOTHING)
    mandal_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mandal_name


class School(models.Model):
    mandal = models.ForeignKey(
        'masters.Mandal', related_name='mandal', on_delete=models.DO_NOTHING)
    school_name = models.CharField(max_length=250)
    address = models.TextField(blank=True)
    village = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    category = models.ForeignKey(
        'masters.SchoolCategory', related_name='category', null=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.school_name, self.village, self.village)


class Designation(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.name


class Vacancy(models.Model):
    school = models.ForeignKey(
        'masters.School', related_name='vacancy_school', on_delete=models.DO_NOTHING)
    designation = models.ForeignKey(
        'masters.Designation', related_name='designation', on_delete=models.DO_NOTHING)
    employee = models.ForeignKey(
        'applications.Application', related_name='alloted_emp', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {} - {} {}'.format(self.employee.first_name, self.employee.last_name, self.school.school_name, self.designation.name)

    def designation_name(self):
        return self.designation.name


class SchoolCategory(models.Model):
    name = models.CharField(max_length=100)
    point = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
