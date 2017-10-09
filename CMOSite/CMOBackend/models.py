# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

import datetime

@python_2_unicode_compatible
class Crisis(models.Model):
	CrisisID = models.IntegerField(primary_key=True)
	Title = models.CharField(max_length=200)
	Location = models.CharField(max_length=200)
	DateTime = models.DateTimeField()
	def __str__(self):
		return self.Title

@python_2_unicode_compatible
class Call(models.Model):
	CrisisID = models.ForeignKey(Crisis, on_delete=models.CASCADE)
	CallID = models.IntegerField(primary_key=True)
	ContactPersonName = models.CharField(max_length=200)
	ContactPersonNumber = models.IntegerField()
	Datetime = models.DateTimeField('date time received')
	BriefDescription = models.CharField()
	def __str__(self):
		return self.BriefDescription(max_length=255)

@python_2_unicode_compatible
class Plan(models.Model):
	CrisisID = models.ForeignKey(Crisis, on_delete=models.CASCADE)
	PlanID = models.IntegerField(primary_key=True)
	isApprovedByPMO = models.BooleanField(initial=False, required=False)
	isApprovedByGeneral = models.BooleanField(initial=False, required=False)
	Datetime = models.DateTimeField('date time of plan submission')
	CrisisType = models.CharField(max_length=200)
	AnalysisOfCase = models.CharField(max_length=255)
	Map = models.URLField('map url')

@python_2_unicode_compatible
class SuggestedActions(models.Model):
	ActionID = models.IntegerField(primary_key=True)
	PlanID = models.ForeignKey(Plan, on_delete=models.CASCADE)
	TypeTroop = models.CharField()
	SeverityLevel = models.IntegerField()

@python_2_unicode_compatible
class Update(models.Model):
	UpdateID = models.IntegerField(primary_key=True)
	CrisisID = models.ForeignKey(Crisis, on_delete=models.CASCADE)
	DateTime = modesl.DateTimeField('Date Published')
	Status = models.CharField()
	Comment = models.CharField()
	Location = models.CharField(max_length=200)
	SeverityLevel = models.IntegerField()
