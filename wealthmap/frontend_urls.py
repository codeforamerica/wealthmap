from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$',
        views.OpportunitySearchCreateView.as_view(),
        name='opportunity-search'
    ),
    url(r'^search/(?P<pk>\d+)/$',
        views.OpportunitySearchDetailView.as_view(),
        name='opportunity-search-detail'
    ),
    url(r'^opportunity/(?P<pk>\d+)/$',
        views.OpportunityDetailView.as_view(),
        name='opportunity-detail'
    ),
    url(r'^opportunity/$',
        views.OpportunityListView.as_view(),
        name='opportunity-list'
    ),
]
