from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'', include('wealthmap.frontend_urls', namespace='wealthmap')),
    url(r'^admin/', admin.site.urls),
    url(r'^wm-api/', include('wealthmap.urls', namespace='wealthmap-api')),
]
