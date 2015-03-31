from django.db import models
from django.contrib.auth.models import User

class Organisation(models.Model):
    TYPES = (
        ("EQ", "Earthquake Specific"),
        ("FI", "Fire Station"),
        ("FL", "Flood Specific"),
        ("TSU", "Tsunami Specific"),
        ("CYC", "Cyclone Specific"),
        ("P", "Police"),
        ("H", "Hospital"),
        ("BB", "Blood Bank"),
        ("NGOS", "NGO Shelter"),
        ("NGOR", "NGO Rescue"),
        ("NGOM", "NGO Medical"),
        ("MISC", "Miscellaneous")
    )

    user = models.OneToOneField(User)
    org_name = models.CharField(max_length = 50)
    org_type = models.CharField(max_length = 4, choices = TYPES)
    description = models.TextField()
    address = models.CharField(max_length = 200)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(Organisation, self).delete(*args, **kwargs)

    def __unicode__(self):
        return self.org_name
