from django.conf.urls import url

from . import views
from . import forms
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about),
    url(r'^gracias/$', views.thanks),
    url(r'^oportunidad/(?P<pk>[0-9]+)/$',
        views.OpportunityDetailView.as_view(),
        name='opportunity-detail'),
    url(r'^preguntas/$', views.SearchFormView.as_view([
        forms.PurposeSearchForm,
        forms.AboutSearchForm,
        forms.IndustrySearchForm,
        forms.LocationSearchForm,
        forms.SizeSearchForm,
    ]), name='search-form',
    ),
    url(r'^preguntas/([0-9]+)/$', views.search_results,
        name='search-results'),
    url(r'^preguntas/([0-9]+)/contacto$', views.ContactFormView.as_view([
        forms.PersonalContactForm,
        forms.BusinessContactForm,
    ]), name='contact-form',
    ),
]
