import datetime

from django.utils import timezone

from embeded_project.celery import app
from food_planner.models import Tank
import serial
from datetime import timedelta, datetime


def is_in_period(set):
    if timezone.now() - timedelta(seconds=10) < set < timezone.now():
        return True
    return False


@app.task
def food_order():
    tanks = Tank.objects.all()
    for tank in tanks:
        if tank.set1_enabled:
            today = timezone.now()
            if is_in_period(tank.set1):
                ser = serial.Serial()
                ser.baudrate = 9600
                ser.port = 'COM' + tank.tank_number + 1
                today.replace(hour=tank.set1.hour, minute=tank.set1.minute, second=tank.set1.second)
                tank.feed_number += 1
                tank.last_feeding_time = today
                tank.save()
                ser.write(bytes(today))
