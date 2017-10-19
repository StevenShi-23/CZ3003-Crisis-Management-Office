# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from .models import Crisis,Call,Plan,SuggestedActions, PlanComments

import datetime, json, requests

PMO_POST_URL = ""
EF_POST_URL = ""

def index(request):
    crisis_set = Crisis.objects.all()
    return render(request,'CMOBackend/index.html', {'crisis_set': crisis_set})


# api should call to .../newCall
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

def gApprovePlan(request, plan_id):
    plan = get_object_or_404(Plan, pk = plan_id)
    plan.isApprovedByGeneral =  True
    changeStatus(plan.CrisisID, Crisis.PLAN_APPROVED_GENERAL)
    plan.save()
    actions = []
    for action in plan.suggestedactions_set.all() :
        actions.append({
            'TroopType' : action.get_TypeTroop_display(),
            'Severity'  : action.SeverityLevel
        })
    planInfo = {
        'PlanID' : plan.id,
        'dateTime' : plan.Datetime,
        'CrisisType' : plan.get_CrisisType_display(),
        'AnalysisOfCase' : plan.AnalysisOfCase,
        'Map' : plan.Map,
        'SuggestedActions' : actions
    }
    # requests.post(PMO_POST_URL, data=planInfo)
    return HttpResponseRedirect(reverse('CMOBackend:index'))

# api should call to .../planFeedback
# json object should be :
# {
# 	"PlanID" : 3,
# 	"Approved" : 'true',
#   "Comments" : "good plan"
# }
@csrf_exempt
def PMOApprove(request):
    json_data = json.loads(request.body)
    plan_id = json_data['PlanID']
    approved = json_data['Approved']
    plan = get_object_or_404(Plan, pk = plan_id)
    comments, created=PlanComments.objects.get_or_create(
        PlanID = plan,
        Comment = json_data['Comments'],
    )
    if (plan.CrisisID.CrisisStatus != Crisis.PLAN_APPROVED_GENERAL) :
        return JsonResponse({'received': False})
    if (approved == 'True') :
        changeStatus(plan.CrisisID, Crisis.PLAN_APPROVED_PMO)
        plan.isApprovedByPMO = True
        plan.save()
    else :
        plan.isApprovedByGeneral = False
        changeStatus(plan.CrisisID, Crisis.PLAN_REJECTED_PMO)
    return JsonResponse({'received': True})

def activatePlan(request, plan_id) :
    plan = get_object_or_404(Plan, pk = plan_id)
    crisis = plan.CrisisID
    changeStatus(plan.CrisisID, "PA")
    print(request.POST['lat'])
    actions = []
    for action in plan.suggestedactions_set.all() :
        actions.append({
            'TroopType' : action.get_TypeTroop_display(),
            'Severity'  : action.SeverityLevel
        })
    EFActivation = {
        'CrisisID' : crisis.id,
        'PlanID' : plan.id,
        'CrisisType' : plan.CrisisType,
        'Description' : plan.AnalysisOfCase,
        'Lat': request.POST['lat'],
        'Lng': request.POST['lng'],
        'SuggestedActions': actions
    }
    # requests.post(EF_POST_URL, data=EFActivation)
    return HttpResponseRedirect(reverse('CMOBackend:index'))

def editPlan(request, crisis_id):
    crisis = get_object_or_404(Crisis, pk = crisis_id)
    plan = crisis.plan_set.all()[0]
    troopEnum={}
    for key,value in SuggestedActions.TROOP_CHOICES :
        troopEnum[key] = value
    sevEnum = [1,2,3,4,5]
    return render(request,'CMOBackend/newPlan.html', {'plan': plan, 'crisis' : crisis, 'troopEnum': troopEnum, 'sevEnum' :sevEnum})

def viewPlan(request,crisis_id):
    crisis = get_object_or_404(Crisis, pk = crisis_id)
    plan_set = crisis.plan_set.all()
    if (not plan_set.exists()) :
        return newPlan(request, crisis_id)
    return render(request,'CMOBackend/plan.html', {'plan': plan_set[0], 'crisis' : crisis})

def updatePlan(request, plan_id):
    plan = get_object_or_404(Plan, pk = plan_id)
    changeStatus(plan.CrisisID, "UP")
    pass

def savePlan(request, crisis_id) :
    crisis = get_object_or_404(Crisis, pk = crisis_id)
    plan_set = crisis.plan_set.all()
    if (not plan_set.exists()):
        plan = Plan(
             CrisisID = crisis,
             Datetime = datetime.datetime.today(),
             CrisisType = request.POST['crisis_choices'],
             AnalysisOfCase = request.POST['AnalysisOfCase'],
             Map = "https://cz3003.herokuapp.com/"+str(crisis_id)+"/map"
             )
    else :
        plan = plan_set[0]
    totalActions = int(request.POST['total_input_fields'])
    plan.isApprovedByGeneral = False
    plan.isApprovedByPMO = False
    plan.save()
    plan.suggestedactions_set.all().delete()
    for i in range(1,totalActions) :
        if 'action'+str(i)+'troopType'in request.POST :
            suggested_action = SuggestedActions.objects.create(
            PlanID = plan,
            TypeTroop = request.POST['action'+str(i)+'troopType'],
            SeverityLevel = request.POST['action'+str(i)+'severity'],
            )
    crisis.CrisisStatus = "PF"
    crisis.save()
    return HttpResponseRedirect(reverse('CMOBackend:index'))

def newPlan(request, crisis_id):
    crisis = get_object_or_404(Crisis, pk = crisis_id)
    return render(request, 'CMOBackend/newPlan.html', {'crisis': crisis})

def maps(request):
    crisis_set = Crisis.objects.all()
    return render(request, 'CMOBackend/map',  {'crisis_set': crisis_set})

def map(request, crisis_id):
    crisis = Crisis.objects.filter(pk = crisis_id)
    return render(request,'CMOBackend/map', {'crisis_set' : crisis})

def changeStatus(crisis,newStatus) :
    crisis.CrisisStatus = newStatus
    crisis.save()
    return
