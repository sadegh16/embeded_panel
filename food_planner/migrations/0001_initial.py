# Generated by Django 3.2.5 on 2021-07-14 17:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tank_number', models.IntegerField(choices=[(0, 'مخزن1'), (1, 'مخزن2'), (2, 'مخزن3')], unique=True)),
                ('set1', models.TimeField(default=django.utils.timezone.now, null=True)),
                ('set2', models.TimeField(default=django.utils.timezone.now, null=True)),
                ('set3', models.TimeField(default=django.utils.timezone.now, null=True)),
            ],
        ),
    ]