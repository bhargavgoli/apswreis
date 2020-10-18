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
from .forms import ApplicationForm, SignUpForm, ExistApplicationForm, LoginForm, ChoosePreferenceForm, ApplicationFormFill
from datetime import datetime, timedelta, date
from .sendmail import sendAppMail

from applications.models import Application, TransferAllotment, EmpPreferences
from masters.models import School, SchoolCategory


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def getSchools(user):
    schools = []
    try:
        emp = Application.objects.get(app_ref_no=user.username)
        selectedSch = EmpPreferences.objects.filter(employee=emp)
        prefers = []
        for sch in selectedSch:
            prefers.append(sch.prefer_school_id)
        schools = School.objects.all().exclude(id__in=prefers)
    except School.DoesNotExist:
        pass
    return schools


def getSelectedSchools(user):
    schools = []
    try:
        emp = Application.objects.get(app_ref_no=user.username)
        selectedSch = EmpPreferences.objects.filter(employee=emp)
        prefers = []
        for sch in selectedSch:
            prefers.append(sch.prefer_school_id)
        schools = School.objects.filter(id__in=prefers)
    except School.DoesNotExist:
        pass
    return schools


def calculateExp(doj):
    today = date.today()
    exp = today.year - doj.year - ((today.month, today.day) <
                                   (doj.month, doj.day))
    return exp


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


def pref_app_view(request):
    form = ExistApplicationForm(request.POST or None)
    msg = None

    if request.method == "POST":
        app_ref_no = form["appRefNo"].value()
        if(app_ref_no and not form.is_valid()):
            try:
                app = Application.objects.get(app_ref_no=app_ref_no)
                if app.is_submitted:
                    if app.years_of_exp >= 8:
                        form.fields['appRefNo'].widget.attrs['readonly'] = True
                        form.fields['otp'].widget.attrs['readonly'] = False
                    else:
                        msg = "You are not eligible to choose preference."
                else:
                    msg = "Application not submitted, please submit application to choose preference"
            except Application.DoesNotExist:
                msg = "Invalid Application reference No"
        elif form.is_valid():
            otp = form.cleaned_data.get('otp')
            if otp == "1234":
                user = authenticate(username=app_ref_no,
                                    password="app_"+app_ref_no)
                login(request, user)
                return redirect('/choosepref')
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

    return render(request, "accounts/pref.html", {"form": form, "msg": msg})


def getUserEligibleSchools(user):
    schools = []
    try:
        app = Application.objects.get(app_ref_no=user.username)
        if app.chronic_illness != '0':
            schools = School.objects.all()
        else:
            try:
                category = SchoolCategory.objects.filter(point__lte=app.points)
                schools = School.objects.filter(category__in=category)
            except SchoolCategory.DoesNotExist:
                pass
    except Application.DoesNotExist:
        pass
    return schools


@login_required(login_url='/existapp')
def choose_pref_app_view(request):
    form = ChoosePreferenceForm(request.POST or None)
    msg = None
    smsg = None
    isEnabled = False
    try:
        app = Application.objects.get(app_ref_no=request.user.username)
    except Application.DoesNotExist:
        app = None

    if request.method == "POST":
        if form.is_valid() and app:
            selected_school = form.cleaned_data.get('school')
            try:
                TransferAllotment.objects.get(application=app)
                msg = "You alread saved your preference."
            except TransferAllotment.DoesNotExist:
                if app:
                    allotment = TransferAllotment(
                        application=app,
                        points=app.points,
                        school_id=selected_school)
                    allotment.save()
                    smsg = "Your preference has been saved."

    try:
        allot = TransferAllotment.objects.get(application=app)
        c = []
        school = School.objects.get(id=allot.school_id)
        c.append((school.id, '{} - {}'.format(school.school_name, school.village)))
        form.fields['school'].widget.choices = c
        isEnabled = True
        smsg = "You are already saved your preference."
    except TransferAllotment.DoesNotExist:
        choices = getUserEligibleSchools(request.user)
        c = []
        for choice in choices:
            c.append(
                (choice.id, '{} - {}'.format(choice.school_name, choice.village)))
            form.fields['school'].widget.choices = c
    return render(request, "accounts/choosepref.html", {"form": form, "msg": msg, "smsg": smsg, "isEnabled": isEnabled})


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
                points = 0
                status = 'Pending'
                date_doj = datetime.strptime(doj, '%Y-%m-%d')
                expYrs = calculateExp(date_doj)
                if expYrs >= 8:
                    points = 1
                    print('{} {}'.format(maritalstatus, gender))
                    if maritalstatus == '0' and gender == '2':
                        points += 5
                    if physical == '1':
                        points += 10
                    if chronicillness != '0':
                        points += 1000  # This points is consider as the user can choose any location
                else:
                    status = 'NotEligible'
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
                    created_by=user_ob,
                    years_of_exp=expYrs,
                    status=status,
                    points=points
                )
                app.save()
                # sendAppMail(email, '{} {}'.format(
                #     firstName, lastName), app_ref)
                msg = 'Application Submitted/Saved Successfully'
                # form = ApplicationForm()
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/newapp.html", {"form": form, "msg": msg})


@login_required(login_url='/existapp')
def fill_app(request):
    msg = None
    success = True
    smsg = None
    pmsg = None
    pemsg = None
    if request.method == "POST":
        form = ApplicationFormFill(request.POST)
        if form.is_valid():
            if 'save' in form.data:
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
                status = 'Submitted'
                try:
                    app = Application.objects.get(
                        app_ref_no=request.user.username)
                    print('{} {}'.format(maritalstatus, gender))
                    if maritalstatus == '0' and gender == '2':
                        app.points += 5
                    if physical == '1':
                        app.points += 10
                    app.marital_status = True if maritalstatus == '1' else False
                    app.physical_disabled = True if physical == '1' else False
                    app.chronic_illness = chronicillness
                    app.status = status
                    app.is_submitted = True
                    app.save()
                    smsg = "Your prefeneces has been saved"
                except Application.DoesNotExist:
                    msg = 'Application Not Found.'
            elif 'addprefer' in form.data:
                try:
                    app = Application.objects.get(
                        app_ref_no=request.user.username)
                except Application.DoesNotExist:
                    app = None
                selectedTransfer = form.cleaned_data.get('transferSchools')
                print(selectedTransfer)
                EmpPreferences(prefer_school_id=selectedTransfer,
                               employee=app).save()
                pmsg = "Preference Added Successfully!!"

    try:
        app = Application.objects.get(app_ref_no=request.user.username)
    except Application.DoesNotExist:
        app = None

    if app.is_submitted:
        success = True
        smsg = "You prefences are saved."
        pmsg = "You prefences are saved."

    form = ApplicationFormFill(initial={
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
        "school": app.school,
        "transferSchools": []
    })
    selectedSchool = School.objects.get(id=app.school_id)
    form.fields['school'].widget.choices = [
        (selectedSchool.id, '{} - {}'.format(selectedSchool.school_name, selectedSchool.village))]
    form.fields['gender'].widget.choices = [
        (app.gender, 'Male' if app.gender == '1' else 'Female')]
    choices = getSchools(request.user)
    selectedChoices = getSelectedSchools(request.user)
    c = []
    for choice in choices:
        c.append((choice.id, '{} - {}'.format(choice.school_name, choice.village)))
        form.fields['transferSchools'].widget.choices = c
    return render(request, "accounts/fillapp.html", {"selectedChoices": selectedChoices, "form": form, "pmsg": pmsg, "pemsg": pemsg, "msg": msg, "smsg": smsg, "success": app.is_submitted, 'uname': request.user.username})


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
