# Generated by Django 4.2 on 2023-07-27 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_store_latitude_store_longitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rated_stores',
            name='value',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
