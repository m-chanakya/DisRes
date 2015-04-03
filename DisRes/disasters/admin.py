from django.contrib import admin
from disasters.models import *

admin.site.register(Disaster)
admin.site.register(Observation)
admin.site.register(SOS)
admin.site.register(Response)
