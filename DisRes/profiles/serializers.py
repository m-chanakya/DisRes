from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = { 'password': {'write_only': True} }

class SubscriberListSerializer(serializers.ModelSerializer):
    fname = serializers.CharField(source='user.first_name')
    email = serializers.EmailField(source='user.email')
    class Meta:
        model = Subscriber
        fields = ('id', 'fname', 'email', 'contact')

class OrganisationListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    class Meta:
        model = Organisation
        fields = ('id', 'org_name', 'org_type', 'email', 'contact')

def create_user(validated_data):
    user_data = validated_data.pop('user')
    user = User.objects.create_user(**user_data)
    return (user, validated_data)

def update_user(instance, validated_data):
    user_data = validated_data.pop('user')
    user = instance.user
    user.username = user_data.get('username', user.username)
    user.email = user_data.get('email', user.email)
    user.first_name = user_data.get('first_name', user.first_name)
    user.last_name = user_data.get('last_name', user.last_name)
    if user_data.get('password') is not None:
        user.set_password(user_data.get('password'))
    user.save()
    return validated_data

class SubscriberSerializer(serializer.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Subscriber
    def create(self, validated_data):
        user, subscriber_data = create_user(validated_data)
        subscriber = Subscriber.objects.create(user=user, **subscriber_data)
        return subscriber
    def update(self, instance, validated_data):
        subscriber_data = update_user(instance, validated_data)
        instance.contact = subscriber_data.get('contact', instance.gender)
        instance.save()
        return instance

class OrganisationSubscriber(serializers.ModelSerializer):
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
        instance.contact = org_data.get('contact', instance.contact)
        instance.address = org_data.get('address', instance.address)
        instance.latitude = org_data.get('latitude', instance.latitude)
        instance.longitude = org_data.get('longitude', instance.longitude)
        instance.save()
        return instance
