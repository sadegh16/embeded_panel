from django.conf.urls import url
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html

from food_planner.models import Tank

admin.site.unregister(Group)


class TankAdmin(admin.ModelAdmin):
    list_display = ('tank_number', 'set1', 'set2', 'set3','feed_number','tank_actions')
    readonly_fields = ('tank_number', 'feed_number')

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
        query=Tank.objects.filter(pk=tank_id)
        if len(query)>0:
            tank=query[0]
            tank.feed_number+=1
            tank.save()
        return redirect('/food_planner/tank/')



    def tank_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Open Door</a>',
            reverse('admin:tank-open-door', args=[obj.pk]),
        )
    tank_actions.short_description = 'Tank Actions'
    tank_actions.allow_tags = True




admin.site.register(Tank, TankAdmin)
