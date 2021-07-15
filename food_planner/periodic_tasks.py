from celery import Celery
from django.utils import timezone
from embeded_project.celery import app
from food_planner.models import Tank
import serial
from datetime import timedelta, datetime
import datetime

def is_in_period(set,today):

    if (today - timedelta(seconds=10)).time()<set < today.time():
        return True
    return False


def trigger_micro(tank, today):
    print("sending to microcontroller ...")
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM' + tank.tank_number + 1
    ser.write(bytes(today))


@app.task
def food_order():
    print("running feeding schedule...")
    tanks = Tank.objects.all()
    for tank in tanks:
        if tank.set1_enabled:
            print("1 enabled")
            today = datetime.datetime.now()
            if is_in_period(tank.set1,today):
                today_modified=today.replace(hour=tank.set1.hour, minute=tank.set1.minute, second=tank.set1.second)
                tank.feed_number += 1
                tank.last_feeding_time = today_modified
                tank.save()
                # trigger_micro(tank, today)
                continue

        if tank.set2_enabled:
            print("2 enabled")

            today = datetime.datetime.now()
            if is_in_period(tank.set1,today):
                today_modified=today.replace(hour=tank.set2.hour, minute=tank.set2.minute, second=tank.set2.second)
                tank.feed_number += 1
                tank.last_feeding_time = today_modified
                tank.save()
                # trigger_micro(tank, today)
                continue


        if tank.set3_enabled:
            print("3 enabled")

            today = timezone.now()
            if is_in_period(tank.set1,today):
                today_modified=today.replace(hour=tank.set3.hour, minute=tank.set3.minute, second=tank.set3.second)
                tank.feed_number += 1
                tank.last_feeding_time = today_modified
                tank.save()
                # trigger_micro(tank, today)
                continue



