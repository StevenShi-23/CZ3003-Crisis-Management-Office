from django.conf.urls import url

from . import views

app_name = 'CMOBackend'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<crisis_id>[0-9]+)/plan$', views.plan, name='plan'),
    url(r'^(?P<crisis_id>[0-9]+)/savePlan/$', views.savePlan, name='savePlan'),
]
