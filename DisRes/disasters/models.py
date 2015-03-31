from django.db import models
from django.contrib.auth.models import User
from profiles.models import Organisation

class Disaster(models.Model):
    TYPES = (
        ("EQ", "Earthquake"),
        ("FI", "Fire"),
        ("FL", "Flood"),
        ("TSU", "Tsunami Specific"),
        ("CYC", "Cyclone Specific"),
        ("LS", "Landslide"),
    )

    class Meta:
        ordering = ('-created',)

    created = models.DateTimeField(auto_now_add=True)
    dis_type = models.CharField(max_length = 3, choices = TYPES)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    status = models.BooleanField(default = True)

    def __unicode__(self):
        return dis_type + ' ' + str(created)

class Observation(models.Model):
    class Meta:
        ordering = ('-created',)

    created = models.DateTimeField(auto_now_add=True)
    disaster = models.ForeignKey(Disaster)
    user = models.ForeignKey(User)
    #image
    description = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    
    def __unicode__(self):
        return str(created) + ' ' + self.user.username

class SOS(models.Model):
    class Meta:
        ordering = ('-created',)

    created = models.DateTimeField(auto_now_add=True)
    disaster = models.ForeignKey(Disaster)
    user = models.ForeignKey(User)
    message = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    
    def __unicode__(self):
        return str(created) + ' ' + self.user.username

class Response(models.Model):
    AID_TYPES = (
        ("R", "Rescue"),
        ("S", "Shelter"),
        ("M", "Medical")
    )
    
    class Meta:
        ordering = ('-created',)

    created = models.DateTimeField(auto_now_add=True)
    sos = models.ForeignKey(SOS)
    org = models.ForeignKey(Organisation)
    aid_type = models.CharField(max_length = 1, choices = AID_TYPES)
    response = models.TextField()