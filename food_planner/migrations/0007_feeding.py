# Generated by Django 3.2.5 on 2021-07-15 17:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('food_planner', '0006_alter_tank_last_feeding_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feeding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tank_number', models.IntegerField(choices=[(0, 'مخزن1'), (1, 'مخزن2'), (2, 'مخزن3')], unique=True)),
                ('feeding_time', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
        ),
    ]