from rest_framework import viewsets, mixins
from rest_framework import permissions
from disasters.serializers import *
from disasters.models import *
from disasters.permissions import *

#RADIUS TO BE CHECKED FOR EACH DISASTER TYPE
dist = {"EQ" : 20, "FI" : 20, "FL" : 20, "TSU" : 20, "CYC" : 20, "LS" : 20}
radius = 20

from math import radians, cos, sin, asin, sqrt, atan2

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(float, [lon1, lat1, lon2, lat2])
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
            queryset = queryset.filter(verified = False)
            return queryset
        else:
            queryset = queryset.filter(verified = True)
        lat = self.request.data.get('lat', None)
        lon = self.request.data.get('lon', None)
        if lat is not None and lon is not None:
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
            queryset = queryset.filter(disaster__verified = False)
        else:
            queryset = queryset.filter(disaster__verified = True)
        disaster = self.request.data.get('disaster', None)
        if disaster is not None:
            disaster = Disaster.objects.get(pk=disaster)
            queryset = queryset.filter(disaster=disaster)
        return queryset
    
    def perform_create(self, serializer):
        lat = self.request.data["latitude"]
        lon = self.request.data["longitude"]
        d_type = self.request.data.pop("dis_type")
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
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerSelf,
                          )
    
    def get_queryset(self):
        queryset = SOS.objects.filter(disaster__status = True)
        if self.request.user.is_superuser:
            queryset = queryset.filter(disaster__verified = False)
        else:
            queryset = queryset.filter(disaster__verified = True)
        if hasattr(self.request.user, 'organisation'):
            org = self.request.user.organisation
            if org.org_type in ['P', 'H', 'NGOR', 'NGOM']:
                return queryset
            ids = []
            for sos in queryset:
                if\
                (sos.disaster.dis_type == 'EQ' and org.org_type in ['EQ']) or\
                (sos.disaster.dis_type == 'FI' and org.org_type in ['FI']) or\
                (sos.disaster.dis_type == 'FL' and org.org_type in ['FL', 'NGOS']) or\
                (sos.disaster.dis_type == 'TSU' and org.org_type in ['TSU', 'NGOS']) or\
                (sos.disaster.dis_type == 'CYC' and org.org_type in ['CYC', 'NGOS']) or\
                (sos.disaster.dis_type == 'LS' and org.org_type in ['NGOS']):
                    ids.append(sos.id)
            queryset = queryset.filter(pk__in=ids)

        elif self.request.user.is_superuser:
            disaster = self.request.data.get('disaster', None)
            if disaster is not None:
                disaster = Disaster.objects.get(pk=disaster)
                queryset = queryset.filter(disaster=disaster)
            return queryset

        else:
            queryset = queryset.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        lat = self.request.data["latitude"]
        lon = self.request.data["longitude"]
        d_type = self.request.data.pop("dis_type")
        disaster = None
        for dis in Disaster.objects.all():
            if dis.dis_type == d_type and haversine(dis.longitude, dis.latitude, lon, lat) <= dist[d_type]:
                disaster = dis
                break
        if disaster is None:
            disaster = Disaster.objects.create(dis_type = d_type, latitude = lat, longitude = lon)
        serializer.save(disaster = disaster, user = self.request.user)
    
class ResponseViewSet(viewsets.ModelViewSet):
    serializer_class = ResponseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOrgSelf,
                          )
    
    def get_queryset(self):
        ids = []
        for resp in Response.objects.all():
            if resp.sos.disaster.status == True and resp.sos.disaster.verified == True:
                ids.append(resp.id)
        queryset = Response.objects.filter(pk__in = ids)
        sos = self.request.data.get('sos', None)
        disaster = self.request.data.get('disaster', None)
        if sos is not None:
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
