# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ApplicationForm(forms.Form):
    firstname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        ))
    lastname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        ))

    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))

    gender = forms.CharField(
        widget=forms.Select(
            choices=[('1', 'Male'), ('2', 'FeMale')],
            attrs={
                "placeholder": "Gender",
                "class": "form-control"
            }
        ))

    employeeId = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Employee Id",
                "class": "form-control"
            }
        ))

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone No",
                "class": "form-control"
            }
        ))

    doj = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Date Of Joining (YYYY-MM-DD)",
                "class": "form-control"
            }
        ))

    maritalstatus = forms.CharField(
        widget=forms.Select(
            choices=[('0', 'Single'), ('1', 'Married')],
            attrs={
                "placeholder": "Marital Status",
                "class": "form-control"
            }
        ))

    physical = forms.CharField(
        widget=forms.Select(
            choices=[('0', 'No'), ('1', 'Yes')],
            attrs={
                "placeholder": "Physical Disability",
                "class": "form-control"
            }
        ))

    chronicillness = forms.CharField(
        widget=forms.Select(
            choices=[('0', 'Not Applicable'), ('1', 'Cancer'), ('2', 'Kidney'),
                     ('3', 'Thalassemia'), ('4', 'Others')],
            attrs={
                "placeholder": "Chronic Illness",
                "class": "form-control"
            }
        ))


class ExistApplicationForm(forms.Form):
    appRefNo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Application Refernce No",
                "class": "form-control"
            }
        ))

    otp = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email OTP",
                "class": "form-control",
                "readonly": True
            }
        ))


class SignUpForm(UserCreationForm):
    firstname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        ))
    lastname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        ))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'username',
                  'email', 'password1', 'password2')
