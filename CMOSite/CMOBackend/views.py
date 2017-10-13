# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from .models import Crisis,Call,Plan,SuggestedActions

import datetime, json

def index(request):
    crisis_set = Crisis.objects.all()
    return render(request,'CMOBackend/index.html', {'crisis_set': crisis_set})


# api should call to .../CMOBackend/newCall
# json object should be :
# {
# 	"CrisisID" : 3,
# 	"Title" : "Postman Crisis 2",
# 	"Location" : "NTU",
# 	"ContactPersonName" : "Shi Kai",
# 	"ContactPersonNumber" : 1234567,
# 	"BriefDescription" : "Post request to create a new Crisis and Call"
# }
@csrf_exempt
def newCall(request) :
    # crisis_id is given by 911
    json_data = json.loads(request.body)
    crisis_id = json_data['CrisisID']
    try :
        crisis = Crisis.objects.get(CrisisID = crisis_id)
    except Crisis.DoesNotExist :
        crisis, created = Crisis.objects.get_or_create(
            CrisisID = crisis_id,
            Title = json_data['Title'],
            Location = json_data['Location'],
            DateTime = datetime.datetime.today(),
            Cleared = False
        )
    call = Call(
        CrisisID = crisis,
    	ContactPersonName = json_data['ContactPersonName'],
    	ContactPersonNumber = json_data['ContactPersonNumber'],
    	Datetime = datetime.datetime.today(),
    	BriefDescription = json_data['BriefDescription']
        )
    call.save()

    return JsonResponse({'success': True})

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
    plan.save()
    for i in range(0,totalActions) :
        if 'action'+str(i)+'troopType'in request.POST :
            suggested_action = SuggestedActions.objects.create(
            PlanID = plan,
            TypeTroop = request.POST['action'+str(i)+'troopType'],
            SeverityLevel = request.POST['action'+str(i)+'severity'],
            )

    return HttpResponse(request.POST, content_type='application/json')

def plan(request, crisis_id):
    crisis = get_object_or_404(Crisis, pk = crisis_id)
    return render(request, 'CMOBackend/plan', {'crisis': crisis})

def maps(request):
    crisis_set = Crisis.objects.all()
    return render(request, 'CMOBackend/map',  {'crisis_set': crisis_set})

def map(request, crisis_id):
    crisis = Crisis.objects.filter(pk = crisis_id)
    return render(request,'CMOBackend/map', {'crisis_set' : crisis})
