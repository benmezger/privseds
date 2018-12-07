# Generated by Django 2.1.4 on 2018-12-07 18:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20181207_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='is_scheduled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='email',
            name='send_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]