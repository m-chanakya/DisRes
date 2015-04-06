from rest_framework import serializers
from disasters.models import *
from profiles.serializers import OrganisationSerializer, UserSerializer

class DisasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disaster
        
class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        
class SOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOS
        
class ResponseSerializer(serializers.ModelSerializer):
    sos = SOSSerializer()
    org = OrganisationSerializer()
    class Meta:
        model = Response