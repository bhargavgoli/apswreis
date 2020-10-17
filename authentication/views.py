# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from .forms import ApplicationForm, SignUpForm, ExistApplicationForm
from datetime import datetime

from applications.models import Application


def exist_app_view(request):
    form = ExistApplicationForm(request.POST or None)
    msg = None

    if request.method == "POST":
        app_ref_no = form["appRefNo"].value()
        if(app_ref_no and not form.is_valid()):
            try:
                app = Application.objects.get(app_ref_no=app_ref_no)
                if not app.is_submitted:
                    form.fields['appRefNo'].widget.attrs['readonly'] = True
                    form.fields['otp'].widget.attrs['readonly'] = False
                else:
                    msg = "Application already submitted."
            except Application.DoesNotExist:
                msg = "Invalid Application reference No"
        elif form.is_valid():
            otp = form.cleaned_data.get('otp')
            if otp == "1234":
                user = authenticate(username=app_ref_no,
                                    password="app_"+app_ref_no)
                login(request, user)
                return redirect('/fillapp')
            else:
                form.fields['appRefNo'].widget.attrs['readonly'] = True
                form.fields['otp'].widget.attrs['readonly'] = False
                msg = "Invalid OTP entered"
        else:
            msg = "Enter app reference no."
        # return redirect('/fillapp')
        # print(form)
        # if form.is_valid():
        #     msg = "valid"
        # else:
        #     msg = "Not valid"

    return render(request, "accounts/existapp.html", {"form": form, "msg": msg})


def app_view(request):
    form = ApplicationForm(request.POST or None)
    print(form.errors)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            firstName = form.cleaned_data.get("firstname")
            lastName = form.cleaned_data.get("lastname")
            gender = form.cleaned_data.get("gender")
            employeeId = form.cleaned_data.get("employeeId")
            phone = form.cleaned_data.get("phone")
            doj = form.cleaned_data.get("doj")
            maritalstatus = form.cleaned_data.get("maritalstatus")
            physical = form.cleaned_data.get("physical")
            chronicillness = form.cleaned_data.get("chronicillness")
            email = form.cleaned_data.get("email")
            try:
                isApp = Application.objects.get(employee_id=employeeId)
                msg = "Application alredy created, plz try in Edit/Submit Application"
                form = ApplicationForm()
            except Application.DoesNotExist:
                app_ref = get_random_string().upper()[:8]
                user_ob = get_user_model()(username=app_ref)
                user_ob.set_password("app_"+app_ref)
                user_ob.save()
                app = Application(
                    app_ref_no=app_ref,
                    first_name=firstName,
                    last_name=lastName,
                    gender=gender,
                    employee_id=employeeId,
                    phone_no=phone,
                    date_of_join=doj,
                    email=email,
                    marital_status=maritalstatus,
                    physical_disabled=physical,
                    chronic_illness=chronicillness,
                    created_by=user_ob
                )
                app.save()
                msg = 'Application Submitted/Saved Successfully'
                form = ApplicationForm()
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/newapp.html", {"form": form, "msg": msg})


@login_required(login_url='/existapp')
def fill_app(request):

    msg = None
    success = False

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            firstName = form.cleaned_data.get("firstname")
            lastName = form.cleaned_data.get("lastname")
            gender = form.cleaned_data.get("gender")
            employeeId = form.cleaned_data.get("employeeId")
            phone = form.cleaned_data.get("phone")
            doj = form.cleaned_data.get("doj")
            maritalstatus = form.cleaned_data.get("maritalstatus")
            physical = form.cleaned_data.get("physical")
            chronicillness = form.cleaned_data.get("chronicillness")
            email = form.cleaned_data.get("email")

            try:
                app = Application.objects.get(
                    app_ref_no=request.user.username)
                app.first_name = firstName
                app.last_name = lastName
                app.gender = gender
                app.employee_id = employeeId
                app.phone_no = phone
                app.email = email
                app.marital_status = True if maritalstatus == '1' else False
                app.physical_disabled = True if physical == '1' else False
                app.chronic_illness = chronicillness
                app.is_submitted = True
                app.save()
                msg = "Application alredy submitted"
            except Application.DoesNotExist:
                msg = 'Application Not Found.'

            return redirect("/logout/")
        else:
            msg = 'Form is not valid'
    else:
        try:
            app = Application.objects.get(app_ref_no=request.user.username)
        except Application.DoesNotExist:
            app = None

        form = ApplicationForm({
            "firstname": app.first_name,
            "lastname": app.last_name,
            "email": app.email,
            "gender": app.gender,
            "employeeId": app.employee_id,
            "phone": app.phone_no,
            "doj": app.date_of_join,
            "maritalstatus": app.marital_status,
            "physical": app.physical_disabled,
            "chronicillness": app.chronic_illness,
        })

    return render(request, "accounts/fillapp.html", {"form": form, "msg": msg, "success": success, 'uname': request.user.username})


def register_user(request):

    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
