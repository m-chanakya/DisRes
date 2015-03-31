from django.conf.urls import patterns, include, url 
from rest_framework import routers
from profiles.views import *
from django.contrib import admin

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'organisations', OrganisationViewSet)

urlpatterns = [ 
    url(r'^', include(router.urls)),
    url(r'auth/$', AuthView.as_view(), name='authenticate'),
    url(r'^admin/', include(admin.site.urls)),
]

