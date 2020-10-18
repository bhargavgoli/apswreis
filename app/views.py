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


def getChornic(id):
    illness = {
        "0": "Not Applicable",
        "1": "Cancer",
        "2": "Kidney",
        "3": "Thalassemia",
        "4": "Others"
    }
    return illness[id]


@login_required(login_url="/newapp/")
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


@login_required(login_url="/newapp/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
