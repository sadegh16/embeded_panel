from celery import Celery
from django.utils import timezone
from embeded_project.celery import app
from food_planner.models import Tank, Feeding
import serial
from datetime import timedelta, datetime
import datetime


def is_in_period(set, today):
    if (today - timedelta(seconds=10)).time() < set < today.time():
        return True
    return False


def trigger_micro(tank, today):
    Feeding.objects.create(tank_number=tank.tank_number,feeding_time=today)
    # print("sending to microcontroller ...")
    # ser = serial.Serial()
    # ser.baudrate = 9600
    # ser.port = '/dev/ttyS' + str(tank.tank_number + 4)
    # ser.open()
    # reformat_today=today.strftime('%Y/%m/%d_%H:%M:%S')
    # ser.write(bytes("N"+reformat_today))
    # ser.close()


@app.task
def reset_tanks():
    print("sending to microcontroller ...")
    tanks = Tank.objects.all()
    for tank in tanks:
        tank.feed_number=0
        tank.save()
    for i in range(3):
        ser = serial.Serial()
        ser.baudrate = 9600
        ser.port = '/dev/ttyS' + str(i + 4)
        ser.open()
        ser.write(bytes("R"))
        ser.close()


@app.task
def food_order():
    print("running feeding schedule...")
    tanks = Tank.objects.all()
    for tank in tanks:
        if tank.set1_enabled:
            print("1 enabled")
            today = datetime.datetime.now()
            if is_in_period(tank.set1, today):
                today_modified = today.replace(hour=tank.set1.hour, minute=tank.set1.minute, second=tank.set1.second)
                tank.feed_number += 1
                tank.last_feeding_time = today_modified
                tank.save()
                trigger_micro(tank, today_modified)
                continue

        if tank.set2_enabled:
            print("2 enabled")

            today = datetime.datetime.now()
            if is_in_period(tank.set2, today):
                today_modified = today.replace(hour=tank.set2.hour, minute=tank.set2.minute, second=tank.set2.second)
                tank.feed_number += 1
                tank.last_feeding_time = today_modified
                tank.save()
                trigger_micro(tank, today_modified)
                continue

        if tank.set3_enabled:
            print("3 enabled")

            today = timezone.now()
            if is_in_period(tank.set3, today):
                today_modified = today.replace(hour=tank.set3.hour, minute=tank.set3.minute, second=tank.set3.second)
                tank.feed_number += 1
                tank.last_feeding_time = today_modified
                tank.save()
                trigger_micro(tank, today_modified)
                continue

