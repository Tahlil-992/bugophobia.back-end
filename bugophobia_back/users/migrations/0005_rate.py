# Generated by Django 3.1.7 on 2021-04-18 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    #dependencies = [
    #    ('users', '0004_baseuser_pro_picture'),
    #]

    operations = [
        migrations.CreateModel(
            name='rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (3, '3'), (4, '4'), (5, '5')], default=0)),
                ('dr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.doctor')),
                ('ur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
            ],
        ),
    ]
