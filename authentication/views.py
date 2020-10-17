# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import ApplicationForm, SignUpForm, ExistApplicationForm


def exist_app_view(request):
    form = ExistApplicationForm(request.POST or None)

    msg = None

    if request.method == "POST":
        return redirect('/fillapp')
        # print(form)
        # if form.is_valid():
        #     msg = "valid"
        # else:
        #     msg = "Not valid"

    return render(request, "accounts/existapp.html", {"form": form, "msg": msg})


def app_view(request):
    form = ApplicationForm(request.POST or None)

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

    return render(request, "accounts/newapp.html", {"form": form, "msg": msg})


# @login_required(login_url='/existapp')
def fill_app(request):

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
        form = ApplicationForm()

    return render(request, "accounts/fillapp.html", {"form": form, "msg": msg, "success": success})


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
