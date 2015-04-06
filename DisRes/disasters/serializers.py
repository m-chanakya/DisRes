from rest_framework import serializers
from disasters.models import *
from profiles.serializers import OrganisationSerializer, UserSerializer

class DisasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disaster
        
class ObservationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    disaster = DisasterSerializer()
    class Meta:
        model = Observation
        extra_kwargs = { 'user': {'read_only': True}, 'disaster': {'read_only': True}}
        
class SOSSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    disaster = DisasterSerializer()
    class Meta:
        model = SOS
        extra_kwargs = { 'user': {'read_only': True}, 'disaster': {'read_only': True}}
        
class ResponseSerializer(serializers.ModelSerializer):
    sos = SOSSerializer()
    org = OrganisationSerializer()
    class Meta:
        model = Response
        extra_kwargs = {'org': {'read_only': True}}