# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from .models import Crisis,Call,Plan,SuggestedActions, PlanComments, Profile, Update

import datetime, json, requests

PMO_URL = "http://118.200.75.51"
PMO_GET_URL = "http://118.200.75.51/api/channels/retrieve/"
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
            DateTime = datetime.datetime.today()
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
    return redirect(PMO_URL)

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
    caseId = json_data['caseid']
    try :
        crisis = Crisis.objects.get(CrisisID = caseId)
    except Crisis.DoesNotExist :
        returnResponse = JsonResponse({'CrisisID does not exist': True})
        returnResponse['Access-Control-Allow-Origin'] = '*'
        return returnResponse

    plan = crisis.plan_set.all()[0]
    r = requests.get(PMO_GET_URL+str(caseId))
    response = r.json()
    if (response['approved']) :
        changeStatus(plan.CrisisID, Crisis.PLAN_APPROVED_PMO)
        plan.isApprovedByPMO = True
    else :
        plan.isApprovedByPMO = False
        plan.isApprovedByGeneral = False
        changeStatus(plan.CrisisID, Crisis.PLAN_REJECTED_PMO)

    plan.save()
    returnResponse = JsonResponse({'received': True})
    returnResponse['Access-Control-Allow-Origin'] = '*'
    return returnResponse

# api should call to .../updatePlan
# json object should be :
# {
    # Crisis ID
    # Status (True , False)
    # Comments
# }
@csrf_exempt
def EFUpdate(request):
    json_data = json.loads(request.body)
    crisis_id = json_data['CrisisID']
    plan_id = json_data['PlanID']
    status = json_data['Status']
    description = json_data['Comments']
    plan = get_object_or_404(Plan, pk = plan_id)

    realStatus = status == "Cleared"
    try :
        crisis = Crisis.objects.get(CrisisID = crisis_id)
    except Crisis.DoesNotExist :
        return JsonResponse({'CrisisID does not exist': True})

    update = Update(
        CrisisID = crisis,
        PlanID = plan,
        Status = status,
        Comment = description,
    )
    update.save()
    if (realStatus) :
        changeStatus(crisis,Crisis.CRISIS_OVER)
    else :
        changeStatus(crisis,Crisis.UPDATE_PENDING)
    return JsonResponse({'received': True})

def activatePlan(request, plan_id) :
    plan = get_object_or_404(Plan, pk = plan_id)
    crisis = plan.CrisisID
    changeStatus(plan.CrisisID, Crisis.PLAN_ACTIVATED)
    actions = []
    for action in plan.suggestedactions_set.all() :
        actions.append({
            'DepartmentType' : action.get_TypeTroop_display(),
            'SeverityRating'  : action.SeverityLevel
        })
    EFActivation = {
        'CrisisID' : crisis.CrisisID,
        'PlanID' : plan.id,
        'CrisisType' : plan.CrisisType,
        'Description' : plan.AnalysisOfCase,
        'Lat': request.POST['lat'],
        'Lon': request.POST['lng'],
        'SuggestedActions': actions
    }
    plan.isApprovedByGeneral = False
    plan.isApprovedByPMO = False
    plan.save()
    headers = {'content-type': 'application/json'}
    r=requests.post('http://efds.herokuapp.com/hq/orderHQ', data=json.dumps(EFActivation), headers=headers)

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
    return render(request,'CMOBackend/plan.html',
                    {
                    'plan': plan_set[0],
                    'crisis' : crisis,
                    'isGeneral' : request.user.profile.role == Profile.GENERAL ,
                    'isAnalyst' : request.user.profile.role == Profile.ANALYST,
                    'isActivated': crisis.CrisisStatus == Crisis.PLAN_ACTIVATED,
                    'isCleared': crisis.CrisisStatus == Crisis.CRISIS_OVER})

def savePlan(request, crisis_id) :
    crisis = get_object_or_404(Crisis, pk = crisis_id)
    plan_set = crisis.plan_set.all()
    if (not plan_set.exists()):
        plan = Plan(
             CrisisID = crisis,
             Datetime = datetime.datetime.today(),
             CrisisType = request.POST['crisis_choices'],
             AnalysisOfCase = request.POST['AnalysisOfCase'],
             Map = "https://cz3003.herokuapp.com/cmo/"+str(crisis.CrisisID)+"/map"
             )
    else :
        plan = plan_set[0]
    totalActions = int(request.POST['total_input_fields'])
    plan.AnalysisOfCase = request.POST['AnalysisOfCase']
    plan.CrisisType = request.POST['crisis_choices']
    plan.Datetime = datetime.datetime.today()
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

@xframe_options_exempt
def map(request, crisis_id):
    crisis = Crisis.objects.get(CrisisID = crisis_id)

    return render(request,'CMOBackend/map', {'crisis_set' : [crisis]})

def changeStatus(crisis,newStatus) :
    crisis.CrisisStatus = newStatus
    crisis.save()
    return

@csrf_exempt
def getPlan(request) :
    json_data = json.loads(request.body)
    crisis_id = json_data['caseid']
    crisis = Crisis.objects.get(CrisisID = crisis_id)
    plan = crisis.plan_set.all()[0]
    actions = plan.suggestedactions_set.all()
    caseDescription = crisis.Title
    caseLocation = crisis.Location

    efForce= ''
    for action in actions :
        efForce= efForce + action.get_TypeTroop_display() +','+ str(action.SeverityLevel)+','
    efForce = efForce [:-1]
    payload = {
        "caseDescription" : caseDescription,
        "caseLocation" : caseLocation,
        "efForce" : efForce
    }
    response = JsonResponse(payload)
    response['Access-Control-Allow-Origin'] = '*'

    return response
