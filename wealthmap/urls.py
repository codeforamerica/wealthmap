from django.conf.urls import url, include
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^opportunity/(?P<pk>\d+)/$', views.OpportunityRAPI.as_view()),
    url(r'^search/$', views.SearchCAPI.as_view()),
    url(r'^search/(?P<pk>\d+)/$', views.SearchRAPI.as_view()),
]
