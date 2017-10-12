# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db import transaction

from .models import Crisis,Call,Plan,SuggestedActions

import datetime

def index(request):
    crisis_set = Crisis.objects.all()
    return render(request,'CMOBackend/index.html', {'crisis_set': crisis_set})

def savePlan(request, crisis_id) :

    plan = Plan(
         CrisisID = get_object_or_404(Crisis, pk = crisis_id),
         Datetime = datetime.datetime.today(),
         CrisisType = request.POST['crisis_choices'],
         AnalysisOfCase = request.POST['AnalysisOfCase'],
         Map = "Https://google.com"
         )
    crisis = get_object_or_404(Crisis, pk = crisis_id)
    totalActions = int(request.POST['total_input_fields']) + 1
    # plan.save()
    # for i in range(0,totalActions) :
    #     if 'action'+str(i)+'troopType'in request.POST :
    #         suggested_action = SuggestedActions.objects.create(
    #         PlanID = plan,
    #         TypeTroop = request.POST['action'+str(i)+'troopType'],
    #         SeverityLevel = request.POST['action'+str(i)+'severity'],
    #         )

    return HttpResponse(request.POST, content_type='application/json')

def plan(request, crisis_id):
    crisis = get_object_or_404(Crisis, pk = crisis_id)
    return render(request, 'CMOBackend/plan.html', {'crisis': crisis})
