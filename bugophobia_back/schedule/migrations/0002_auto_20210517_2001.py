# Generated by Django 3.1.7 on 2021-05-17 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_doctor_visit_duration_time'),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('doctor', 'start_time')},
        ),
    ]
