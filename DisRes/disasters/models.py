from django.db import models

class Disaster(models.Model):
    TYPES = (
        ("E", "Earthquake"),
        ("F", "Fire"),
    )

    class Meta:
        ordering = ('created',)

    created = models.DateTimeField(auto_now_add=True)
    dis_type = models.CharField(max_length = 1, choices = TYPES)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    def __unicode__(self):
        return dis_type + ' ' + str(created)

class Observation(models.Model):
    class Meta:
        ordering = ('created',)

    created = models.DateTimeField(auto_now_add=True)
    disaster = models.ForeignKey(Disaster)
    #image
    description = models.TextField()
    
    def __unicode__(self):
        return str(created)

class SOS(models.Model):
    class Meta:
        ordering = ('created',)

    created = models.DateTimeField(auto_now_add=True)
    disaster = models.ForeignKey(Disaster)
    message = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    
    def __unicode__(self):
        return str(created)
