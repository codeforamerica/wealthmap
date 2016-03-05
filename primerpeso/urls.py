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
    ])),
]
