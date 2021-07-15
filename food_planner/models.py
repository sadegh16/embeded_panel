from django.db import models

# Create your models here.
from django.utils.timezone import now


class Tank(models.Model):
    SUB_TYPES = ((0, 'مخزن1'), (1, 'مخزن2'), (2, 'مخزن3'))
    tank_number = models.IntegerField(choices=SUB_TYPES, unique=True )
    set1 = models.TimeField(default=now, null=True, blank=False)
    set2 = models.TimeField(default=now, null=True, blank=False)
    set3 = models.TimeField(default=now, null=True, blank=False)
    set1_enabled = models.BooleanField(default=False,)
    set2_enabled = models.BooleanField(default=False,)
    set3_enabled = models.BooleanField(default=False,)
    last_feeding_time = models.DateTimeField(default=now, null=True, blank=False)
    feed_number = models.IntegerField(default=0,)