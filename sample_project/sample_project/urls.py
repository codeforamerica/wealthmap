from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^test-api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('wealthmap.urls')),
]
