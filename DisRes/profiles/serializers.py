from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = { 'password': {'write_only': True} }

def create_user(validated_data):
    user_data = validated_data.pop('user')
    user = User.objects.create_user(**user_data)
    return (user, validated_data)

def update_user(instance, validated_data):
    user_data = validated_data.pop('user')
    user = instance.user
    user.username = user_data.get('username', user.username)
    user.email = user_data.get('email', user.email)
    if user_data.get('password') is not None:
        user.set_password(user_data.get('password'))
    user.save()
    return validated_data

class OrganisationListSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(source='user.username')
    class Meta:
        model = Organisation
        fields = ('id', 'org_name', 'org_type', 'mobile')

class OrganisationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Organisation
    def create(self, validated_data):
        user, org_data = create_user(validated_data)
        org = Organisation.objects.create(user=user, **org_data)
        return org
    def update(self, instance, validated_data):
        org_data = update_user(instance, validated_data)
        instance.org_name = org_data.get('org_name', instance.org_name)
        instance.org_type = org_data.get('org_type', instance.org_type)
        instance.description = org_data.get('description', instance.description)
        instance.address = org_data.get('address', instance.address)
        instance.latitude = org_data.get('latitude', instance.latitude)
        instance.longitude = org_data.get('longitude', instance.longitude)
        instance.save()
        return instance
