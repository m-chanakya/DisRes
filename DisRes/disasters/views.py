from rest_framework import viewsets
from rest_framework import permissions
from disasters.serializers import *
from disasters.models import *
from disasters.permissions import *

class DisasterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DisasterSerializer
    
    def get_queryset(self):
        return Disaster.objects.filter(status = True)

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

class ObservationViewSet(viewsets.ModelViewSet):
    serializer_class = ObservationSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerSelf,
                          )
    
    def get_queryset(self):
        return Observation.objects.filter(disaster__status = True)
    
    def perform_create(self, serializer):
        pass

class SOSViewSet(viewsets.ModelViewSet):
    serializer_class = SOSSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerSelf,
                          )
    
    def get_queryset(self):
        return SOS.objects.filter(disaster__status = True)
    
class ResponseViewSet(viewsets.ModelViewSet):
    serializer_class = SOSSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerSelf,
                          )
    
    def get_queryset(self):
        return SOS.objects.filter(disaster__status = True)
