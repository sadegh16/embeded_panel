from embeded_project.celery import app


from food_planner.periodic_tasks import trigger_micro


@app.task
def send_open_door(tank,raw_time,):
    trigger_micro(tank,raw_time,)