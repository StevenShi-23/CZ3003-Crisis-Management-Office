from django.conf.urls import include, url

from . import views

app_name = 'CMOBackend'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^newCall$', views.newCall, name='newCall'),
    url(r'^(?P<crisis_id>[0-9]+)/plan/new$', views.newPlan, name='newPlan'),
    url(r'^(?P<plan_id>[0-9]+)/plan/general_approve$', views.gApprovePlan, name='gApprovePlan'),
    url(r'^(?P<plan_id>[0-9]+)/plan/activate$', views.activatePlan, name='activatePlan'),
    url(r'^(?P<crisis_id>[0-9]+)/plan$', views.viewPlan, name='viewPlan'),
    url(r'^(?P<crisis_id>[0-9]+)/savePlan$', views.savePlan, name='savePlan'),
    url(r'^maps$', views.maps, name='maps'),
    url(r'^(?P<crisis_id>[0-9]+)/map$', views.map, name='map'),
    url(r'^(?P<crisis_id>[0-9]+)/plan/edit$', views.editPlan, name='editPlan'),
    url(r'^planFeedback$', views.PMOApprove, name='PMOApprove'),
]