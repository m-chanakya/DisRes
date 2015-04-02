from rest_framework import viewsets
from rest_framework import permissions
from profiles.serializers import *
from profiles.models import Organisation
from django.contrib.auth.models import User
from profiles.permissions import *

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserSelf,)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        user = self.request.data
        user = authenticate(username=user['username'], password=user['password'])
        login(self.request, user)
    
class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    permission_classes = (IsOrganisationSelf,)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrganisationListSerializer
        return OrganisationSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        user = self.request.data['user']
        user = authenticate(username=user['username'], password=user['password'])
        login(self.request, user)
    
def logged_in(user):
    response = {"status" : "logged in"}
    if hasattr(user, 'organisation'):
        response["id"] = user.organisation.id
        response["user_type"] = "organisation"
    else:
        response["id"] = user.id
        response["user_type"] = "user"
    return response


class AuthView(APIView):
    def get(self, request):
        if request.user.is_authenticated():
            return Response(logged_in(request.user))
        else:
            return Response({"status" : "not logged in"})

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(logged_in(user))
        else:
            return Response({"status" : "invalid credentials"})

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({"status" : "logged out"})
