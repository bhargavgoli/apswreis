# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from applications.models import Application
from authentication.forms import ApplicationForm
from masters.models import School, SchoolCategory, Vacancy
from authentication.sendmail import sendAppMail
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from datetime import datetime, date


def getChornic(id):
    illness = {
        "0": "Not Applicable",
        "1": "Cancer",
        "2": "Kidney",
        "3": "Thalassemia",
        "4": "Others"
    }
    return illness[id]


@login_required(login_url="/existapp")
def index(request):
    context = {}
    context['segment'] = 'index'
    try:
        apps = Application.objects.all()
    except Application.DoesNotExist:
        apps = []
    html_template = loader.get_template('index.html')
    parseApps = []
    for app in apps:
        app.gender = 'Male' if app.gender == '1' else 'Female'
        app.marital_status = 'Married' if app.marital_status else 'Single'
        app.physical_disabled = 'Yes' if app.physical_disabled else 'No'
        app.chronic_illness = getChornic(app.chronic_illness)
        parseApps.append(app)
    context['apps'] = parseApps
    return HttpResponse(html_template.render(context, request))


def getNewAppContext(context, request):
    context['form'] = ApplicationForm(request.POST or None)
    context['msg'] = None
    return context


def getSchools():
    schools = []
    try:
        schools = School.objects.all()
    except School.DoesNotExist:
        pass
    return schools


def calculateExp(doj):
    today = date.today()
    exp = today.year - doj.year - ((today.month, today.day) <
                                   (doj.month, doj.day))
    return exp


@login_required(login_url='/existapp')
def app_view(request):
    form = ApplicationForm(request.POST or None)
    print(form.errors)
    msg = None
    smsg = None
    if request.method == "POST":
        if form.is_valid():
            firstName = form.cleaned_data.get("firstname")
            lastName = form.cleaned_data.get("lastname")
            gender = form.cleaned_data.get("gender")
            employeeId = form.cleaned_data.get("employeeId")
            phone = form.cleaned_data.get("phone")
            doj = form.cleaned_data.get("doj")
            dob = form.cleaned_data.get("dob")
            maritalstatus = form.cleaned_data.get("maritalstatus")
            physical = form.cleaned_data.get("physical")
            chronicillness = form.cleaned_data.get("chronicillness")
            email = form.cleaned_data.get("email")
            school = form.cleaned_data.get("school")
            try:
                isApp = Application.objects.get(employee_id=employeeId)
                msg = "Employee alredy created."
                form = ApplicationForm()
            except Application.DoesNotExist:
                app_ref = get_random_string().upper()[:8]
                user_ob = get_user_model()(username=app_ref)
                user_ob.set_password("app_"+app_ref)
                user_ob.save()
                points = 0
                status = 'Pending'
                expYrs = calculateExp(doj)
                try:
                    sch = School.objects.get(id=school)
                    schcategory = SchoolCategory.objects.get(
                        id=sch.category_id)
                except School.DoesNotExist:
                    sch = None
                except SchoolCategory.DoesNotExist:
                    schcategory = None
                if schcategory:
                    points = schcategory.point
                if expYrs >= 8:
                    print('{} {}'.format(maritalstatus, gender))
                    if maritalstatus == '0' and gender == '2':
                        points += 5
                    if physical == '1':
                        points += 10

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
                        chronic_illness='0',
                        created_by=user_ob,
                        years_of_exp=expYrs,
                        status=status,
                        points=points,
                        school=sch,
                        date_of_birth=dob
                    )
                    app.save()
                    sendAppMail(email, '{} {}'.format(
                        firstName, lastName), app_ref)
                    form = ApplicationForm()
                    smsg = 'Employee saved successfully and sent email with ref no'
                else:
                    msg = 'Employee is not eligible for transfer.'
        else:
            msg = 'Error validating the form'

    choices = getSchools()
    c = []
    for choice in choices:
        c.append(
            (choice.id, '{} - {}'.format(choice.school_name, choice.village)))
        form.fields['school'].widget.choices = c
    return render(request, "newapp.html", {"form": form, "msg": msg, 'segment': 'newapp', 'smsg': smsg})


@login_required(login_url='/')
def transfers_view(request):
    list = []
    try:
        list = Vacancy.objects.all()
    except:
        pass
    return render(request, "ui-transfers.html", {"segment": 'transfers', 'list': list})


@login_required(login_url="/existapp")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        if load_template == "newapp.html":
            context = getNewAppContext(context, request)
        print(context)
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
