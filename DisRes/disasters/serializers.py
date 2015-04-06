from rest_framework import serializers
from disasters.models import *
from profiles.serializers import OrganisationSerializer, UserSerializer

class DisasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disaster
        
class ObservationSerializer(serializers.ModelSerializer):
    dis_type = serializers.CharField(source='disaster.dis_type')
    class Meta:
        model = Observation
        exclude = ('user', 'disaster')
        
class SOSSerializer(serializers.ModelSerializer):
    dis_type = serializers.CharField(source='disaster.dis_type')
    class Meta:
        model = SOS
        exclude = ('user', 'disaster')
        
class ResponseSerializer(serializers.ModelSerializer):
    sos_id = serializers.CharField(source='sos.id')
    org_name = serializers.CharField(source='org.org_name', read_only=True)
    org_type = serializers.CharField(source='org.org_type', read_only=True)
    class Meta:
        model = Response
        exclude = ('org', 'sos')