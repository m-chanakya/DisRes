from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = { 'password': {'write_only': True} }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

def create_user(validated_data):
    user_data = validated_data.pop('user')
    user = User.objects.create_user(**user_data)
    return (user, validated_data)

def update_user(instance, validated_data):
    user_data = validated_data.pop('user')
    user = instance.user
    for attr, value in user_data.items():
        if attr == 'password':
            user.set_password(value)
        else:
            setattr(user, attr, value)
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
        for attr, value in org_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
