from rest_framework import serializers
from disasters.models import *

class DisasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disaster
        exclude = ('created')
        
class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        extra_kwargs = { 'user': {'read_only': True},
                         'disaster' : {'read_only' : True},
                        }
        
class SOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOS
        extra_kwargs = { 'user': {'read_only': True},
                         'disaster' : {'read_only' : True},
                        }
        
class SOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        extra_kwargs = { 'org': {'read_only': True},}