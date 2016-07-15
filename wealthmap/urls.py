from django.conf.urls import url, include
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^opportunity/(?P<pk>\d+)/$', views.OpportunityRAPI.as_view()),
    url(r'^benefit-type/$', views.BenefitTypeLAPI.as_view()),
    url(r'^benefit-type/(?P<pk>\d+)/$', views.BenefitTypeRAPI.as_view()),
    url(r'^purpose/$', views.PurposeLAPI.as_view()),
    url(r'^purpose/(?P<pk>\d+)/$', views.PurposeRAPI.as_view()),
    url(r'^industry/$', views.IndustryLAPI.as_view()),
    url(r'^industry/(?P<pk>\d+)/$', views.IndustryRAPI.as_view()),
    url(r'^search/$', views.SearchCAPI.as_view()),
    url(r'^search/(?P<pk>\d+)/$', views.SearchRAPI.as_view()),
]
