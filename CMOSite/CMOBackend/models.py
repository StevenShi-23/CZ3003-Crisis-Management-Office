# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MaxValueValidator, MinValueValidator

import datetime
import urllib2
import json
from pprint import pprint
import os


@python_2_unicode_compatible
class Crisis(models.Model):
	CrisisID = models.IntegerField(default=000)
	Title = models.CharField(max_length=200)
	Location = models.CharField(max_length=200)
	DateTime = models.DateTimeField()
	PLAN_ACTIVATED = 'PA'
	PLAN_FORMED = 'PF'
	PLAN_APPROVED_GENERAL = 'PAG'
	PLAN_APPROVED_PMO = 'PAP'
	CRISIS_OVER = "CO"
	UPDATE_PENDING = "UP"
	NEW_CRISIS = "NC"
	CRISIS_STATUS=(
        (NEW_CRISIS, 'New Crisis, Awaiting Plan'),
        (PLAN_FORMED, 'Plan Formed, Awaiting Authorization'),
        (PLAN_APPROVED_GENERAL, 'Approved by General, Awaiting Authorization'),
        (PLAN_APPROVED_PMO, 'Authorized, Awaiting Activation'),
        (PLAN_ACTIVATED, 'Plan In Action'),
        (UPDATE_PENDING, 'New Update Received'),
        (CRISIS_OVER, 'Crisis Cleared'),
    )
	CrisisStatus = models.CharField(max_length=3, choices=CRISIS_STATUS, default="NC")

	def __str__(self):
		return self.Title

	def toLatLng(self):
		urlString = "https://maps.googleapis.com/maps/api/geocode/json?address="+self.Location+"&key="+'AIzaSyAxmNbmdGzDgu_sdi7Je0ENXOmDm80P7wU'
		response = urllib2.urlopen(urlString)
		data = json.load(response)
		# latlng = {
		# 	lat : ...,
		# 	lng : ...
		# }
		return (data["results"][0]["geometry"]["location"])

@python_2_unicode_compatible
class Call(models.Model):
	CrisisID = models.ForeignKey(Crisis, on_delete=models.CASCADE)
	ContactPersonName = models.CharField(max_length=200, blank=True)
	ContactPersonNumber = models.IntegerField(blank=True)
	Datetime = models.DateTimeField('date time received')
	BriefDescription = models.TextField()

	def __str__(self):
		return self.BriefDescription

# @python_2_unicode_compatible
class Plan(models.Model):
	TERRORIST = 'TR'
	NATURAL_DISASTER = 'ND'
	EPIDEMIC = 'EP'
	CRISIS_CHOICES=(
        (TERRORIST, 'Terrorist'),
        (NATURAL_DISASTER, 'Natural Disaster'),
        (EPIDEMIC, 'Epidemic'),
    )
	CrisisID = models.ForeignKey(Crisis, on_delete=models.CASCADE)
	isApprovedByPMO = models.BooleanField(default=False, blank=True)
	isApprovedByGeneral = models.BooleanField(default=False, blank=True)
	Datetime = models.DateTimeField('date time of plan submission')
	CrisisType = models.CharField(max_length=2, choices=CRISIS_CHOICES)
	AnalysisOfCase = models.TextField()
	Map = models.URLField('map url')
	def __str__(self):
		return self.CrisisID.Title

# @python_2_unicode_compatible
class SuggestedActions(models.Model):

	MILITARY = 'MIL'
	BOMB_DISPOSAL = 'BDP'
	COAST_GUARD = 'CGD'
	HAZMAT = 'HAZ'
	SEARCH_AND_RESCUE = 'SNR'
	CIVILIAN_EVAC = 'CEV'
	AMBULANCE = 'AMB'
	EMERGENCY_TRAFFIC_CONTRL = 'ETC'
	FIREFIGHTING = 'FFT'
	INFECTIOUS_DISEASE_QUARANTINE = 'IDQ'
	TROOP_CHOICES = (
        (MILITARY, 'Military'),
        (BOMB_DISPOSAL, 'Bomb Disposal'),
        (COAST_GUARD, 'Coast Guard'),
        (HAZMAT, 'Hazmat'),
        (SEARCH_AND_RESCUE, 'Search and Rescue'),
        (CIVILIAN_EVAC, 'Civilian Evacuation'),
        (AMBULANCE, 'Ambulance'),
        (EMERGENCY_TRAFFIC_CONTRL, 'Emergency Traffic Control'),
        (FIREFIGHTING, 'Firefighters'),
        (INFECTIOUS_DISEASE_QUARANTINE, 'Infectious Disease Quarantine Personnel'),
    )
	PlanID = models.ForeignKey(Plan, on_delete=models.CASCADE)
	TypeTroop = models.CharField(
		max_length=3,
		choices=TROOP_CHOICES)
	SeverityLevel = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])

# @python_2_unicode_compatible
class Update(models.Model):
	CrisisID = models.ForeignKey(Crisis, on_delete=models.CASCADE)
	DateTime = models.DateTimeField('Date Published')
	Status = models.CharField(max_length=10)
	Comment = models.CharField(max_length=255)
	Location = models.CharField(max_length=200)
	SeverityLevel = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
