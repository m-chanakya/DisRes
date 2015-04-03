from rest_framework import viewsets, mixins
from rest_framework import permissions
from disasters.serializers import *
from disasters.models import *
from disasters.permissions import *

#DISTANCES
dist = {"EQ" : 10, "FI" : 10, "FL" : 10, "TSU" : 10, "CYC" : 10, "LS" : 10}
radius = 10

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

class DisasterViewSet(viewsets.ModelViewSet):
    serializer_class = DisasterSerializer
    permission_classes = (IsAdminOrReadOnly,)
    
    def get_queryset(self):
        queryset = Disaster.objects.filter(status = True)
        if self.request.user.is_superuser:
            queryset.filter(verified = False)
            return queryset
        else:
            queryset.filter(verified = True)
        lat = self.request.data.get('lat', None)
        lon = self.request.data.get('lon', None)
        if lat is not None and lon is not None:
            self.request.data.pop('lat')
            self.request.data.pop('lon')
            ids = []
            for dis in queryset:
                if haversine(dis.longitude, dis.latitude, lon, lat) <= radius:
                    ids.append(dis.id)
            queryset = queryset.filter(pk__in=ids)
        return queryset

class ObservationViewSet(viewsets.ModelViewSet):
    serializer_class = ObservationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerSelf,
                          )
    
    def get_queryset(self):
        queryset = Observation.objects.filter(disaster__status = True)
        if self.request.user.is_superuser:
            queryset.filter(disaster__verified = False)
        else:
            queryset.filter(disaster__verified = True)
        disaster = self.request.data.get('disaster', None)
        if disaster is not None:
            self.request.data.pop('disaster')
            disaster = Disaster.objects.get(pk=disaster)
            queryset = queryset.filter(disaster=disaster)
        return queryset
    
    def perform_create(self, serializer):
        lat = self.request.data["latitude"]
        lon = self.request.data["longitude"]
        d_type = self.request.data.pop["dis_type"]
        disaster = None
        for dis in Disaster.objects.all():
            if dis.dis_type == d_type and haversine(dis.longitude, dis.latitude, lon, lat) <= dist[d_type]:
                disaster = dis
                break
        if disaster is None:
            disaster = Disaster.objects.create(dis_type = d_type, latitude = lat, longitude = lon)
        serializer.save(disaster = disaster, user = self.request.user)
        
class SOSViewSet(viewsets.ModelViewSet):
    serializer_class = SOSSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerSelf,
                          )
    
    def get_queryset(self):
        queryset = Observation.objects.filter(disaster__status = True)
        if self.request.user.is_superuser:
            queryset.filter(disaster__verified = False)
        else:
            queryset.filter(disaster__verified = True)
        disaster = self.request.data.get('disaster', None)
        if disaster is not None:
            self.request.data.pop('disaster')
            disaster = Disaster.objects.get(pk=disaster)
            queryset = queryset.filter(disaster=disaster)
        return queryset
    
    def perform_create(self, serializer):
        lat = self.request.data["latitude"]
        lon = self.request.data["longitude"]
        d_type = self.request.data.pop["dis_type"]
        disaster = None
        for dis in Disaster.objects.all():
            if dis.dis_type == d_type and haversine(dis.longitude, dis.latitude, lon, lat) <= dist[d_type]:
                disaster = dis
                break
        if disaster is None:
            disaster = Disaster.objects.create(dis_type = d_type, latitude = lat, longitude = lon)
        serializer.save(disaster = disaster, user = self.request.user)
    
class ResponseViewSet(viewsets.ModelViewSet):
    serializer_class = SOSSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOrgSelf,
                          )
    
    def get_queryset(self):
        queryset = Observation.objects.filter(disaster__status = True, disaster__verified = True)
        sos = self.request.data.get('sos', None)
        disaster = self.request.data.get('disaster', None)
        if sos is not None:
            self.request.data.pop('sos')
            self.request.data.pop('disaster')
            sos = SOS.objects.get(pk=sos)
            queryset = queryset.filter(sos=sos)
        elif disaster is not None:
            disaster = Disaster.objects.get(pk=disaster)
            queryset = queryset.filter(sos__disaster=disaster)
        return queryset
    
    def perform_create(self, serializer):
        sos = self.request.data.pop("sos")
        sos = SOS.objects.get(pk=sos)
        org = self.request.user.organisation
        serializer.save(sos = sos, org = org)