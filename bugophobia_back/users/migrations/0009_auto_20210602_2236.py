# Generated by Django 3.1.7 on 2021-06-02 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_merge_20210530_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='rate_avg',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='pro_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='officephone',
            name='office',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone', to='users.office'),
        ),
    ]
