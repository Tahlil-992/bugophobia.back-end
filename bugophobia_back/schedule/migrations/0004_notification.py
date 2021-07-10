# Generated by Django 3.1.7 on 2021-06-15 07:24

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_merge_20210615_1149'),
        ('schedule', '0003_reservation_office'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime(2021, 6, 15, 7, 24, 53, 248781, tzinfo=utc))),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.reservation')),
            ],
        ),
    ]
