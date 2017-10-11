# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .models import Crisis,Call,Plan,SuggestedActions

import datetime

def index(request):
    return render(request,'CMOBackend/index.html')
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def savePlan(request, crisis_id) :

    # plan = Plan(
    #     CrisisID = crisis_id,
    #     Datetime = datetime.datetime.today(),
    #     CrisisType = 'NA',
    #     AnalysisOfCase = "to be filled",
    #     Map = "Https://google.com"
    # )
    # plan.save()
    print (request.POST)
    #
    # suggested_action = SuggestedActions(
    #     PlanID = plan.PlanID,
    #     TypeTroop = '',
    #     SeverityLevel = ''
    # )
    return HttpResponse(request.POST, content_type='application/json')

def plan(request, crisis_id):
    crisis = get_object_or_404(Crisis, pk = crisis_id)
    return render(request, 'CMOBackend/plan.html', {'crisis': crisis})
