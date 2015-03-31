# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('org_name', models.CharField(max_length=50)),
                ('org_type', models.CharField(max_length=4, choices=[(b'EQ', b'Earthquake Specific'), (b'FI', b'Fire Station'), (b'FL', b'Flood Specific'), (b'TSU', b'Tsunami Specific'), (b'CYC', b'Cyclone Specific'), (b'P', b'Police'), (b'H', b'Hospital'), (b'BB', b'Blood Bank'), (b'NGOS', b'NGO Shelter'), (b'NGOR', b'NGO Rescue'), (b'NGOM', b'NGO Medical')])),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=200)),
                ('latitude', models.DecimalField(max_digits=10, decimal_places=6)),
                ('longitude', models.DecimalField(max_digits=10, decimal_places=6)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
