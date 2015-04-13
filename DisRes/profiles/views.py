from rest_framework import viewsets
from rest_framework import permissions
from profiles.serializers import *
from profiles.models import Organisation
from disasters.models import Disaster
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
        user = self.request.data.get('user', None)
        if user:
            username = user.get('username', None)
            password = user.get('password', None)
            if username and password:
                user = authenticate(username=username, password=password)
                login(self.request, user)
                return Response(logged_in(user))
            else:
                return Response({"status" : "invalid credentials"})
        else:
            return Response({"status" : "invalid credentials"})

class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    permission_classes = (IsOrganisationSelf,)

    def get_serializer_class(self):
        disaster = self.request.META.get('HTTP_DISASTER', None)
        if disaster:
            return OrganisationEmailSerializer
        elif self.action == 'list':
            return OrganisationListSerializer
        return OrganisationSerializer

    def get_queryset(self):
        queryset = Organisation.objects.all()
        disaster = self.request.META.get('HTTP_DISASTER', None)
        if disaster:
            disaster = Disaster.objects.get(pk=disaster)
            types = ['P', 'H', 'NGOR', 'NGOM']
            d_type = disaster.dis_type
            if d_type == 'EQ':
                types.extend(['EQ'])
            elif d_type == 'FI':
                types.extend(['FI'])
            elif d_type == 'FL':
                types.extend(['FL', 'NGOS'])
            elif d_type == 'TSU':
                types.extend(['FL', 'NGOS'])
            elif d_type == 'CYC':
                types.extend(['CYC', 'NGOS'])
            elif d_type == 'LS':
                types.extend(['NGOS'])
            ids = []
            for org in Organisation.objects.all():
                if org.org_type in types:
                    ids.append(org.id)
            queryset = queryset.filter(pk__in=ids)
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        user = self.request.data.get('user', None)
        if user:
            username = user.get('username', None)
            password = user.get('password', None)
            if username and password:
                user = authenticate(username=username, password=password)
                login(self.request, user)
                return Response(logged_in(user))
            else:
                return Response({"status" : "invalid credentials"})
        else:
            return Response({"status" : "invalid credentials"})

def logged_in(user):
    response = {"status" : "logged in"}
    if user.is_superuser:
        response["id"] = user.id
        response["user_type"] = "admin"
    elif hasattr(user, 'organisation'):
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
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = None
        if username and password:
            user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(logged_in(user))
        else:
            return Response({"status" : "invalid credentials"})

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({"status" : "logged out"})