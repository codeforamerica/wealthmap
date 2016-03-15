from django.conf.urls import url

from . import views
from . import forms
urlpatterns = [
    url(r'^about/$', views.about),
    url(r'^preguntas/$', views.SearchFormView.as_view([
        forms.PurposeSearchForm,
        forms.AboutSearchForm,
        forms.IndustrySearchForm,
        forms.LocationSearchForm,
        forms.SizeSearchForm,
    ]), name='search-form',
    ),
    url(r'^opportunities/(?P<pk>[0-9]+)/$', views.OpportunityDetailView.as_view(), name='opportunity-detail'),
    url(r'^results/([0-9]+)/$', views.search_results, name='search-results'),
]
