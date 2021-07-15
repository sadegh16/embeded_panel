from django.conf.urls import url
from django.contrib import admin
from django.utils import timezone
# Register your models here.
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from food_planner.models import Tank
from django.contrib import messages
import datetime
from datetime import timedelta

from food_planner.periodic_tasks import trigger_micro

admin.site.unregister(Group)


class TankAdmin(admin.ModelAdmin):
    list_display = ('tank_number', 'set1', 'set2', 'set3', 'feed_number', 'last_feeding_time', 'tank_actions')
    readonly_fields = ('tank_number', 'feed_number', 'last_feeding_time')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<tank_id>.+)/open-door/$',
                self.admin_site.admin_view(self.process_open_door),
                name='tank-open-door',
            ),

        ]
        return custom_urls + urls

    def process_open_door(self, request, tank_id, *args, **kwargs):
        query = Tank.objects.filter(pk=tank_id)
        if len(query) > 0 :
            tank = query[0]
            now=timezone.now()
            if tank.last_feeding_time +timedelta(seconds=10)< now:
                tank.feed_number += 1
                raw_time=datetime.datetime.now()
                tank.last_feeding_time = raw_time
                tank.save()
                # trigger_micro(tank,raw_time,)
        return redirect('/food_planner/tank/')

    def tank_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Open Door</a>',
            reverse('admin:tank-open-door', args=[obj.pk]),
        )

    tank_actions.short_description = 'Tank Actions'
    tank_actions.allow_tags = True


admin.site.register(Tank, TankAdmin)
