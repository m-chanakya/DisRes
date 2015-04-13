from django.conf.urls import patterns, include, url
from rest_framework import routers
from profiles.views import *
from disasters.views import *
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'organisations', OrganisationViewSet, base_name = "organisations")
router.register(r'disasters', DisasterViewSet, base_name = "disasters")
router.register(r'observations', ObservationViewSet, base_name = "observations")
router.register(r'sos', SOSViewSet, base_name = "sos")
router.register(r'responses', ResponseViewSet, base_name = "responses")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'auth/$', AuthView.as_view(), name='authenticate'),
    #url('disaters/(?P<lat>\d+\.?\d+)/(?P<lon>\d+\.?\d+)/$', DisasterViewSet.as_view()),
    #url('observations/(?P<disaster>\d+)/$', ObservationViewSet.as_view()),
    #url('sos/(?P<disaster>\d+)/$', SOSViewSet.as_view()),
    #url('responses/(?P<disaster>\d+)/(?P<sos>\d+)/$', ResponseViewSet.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
