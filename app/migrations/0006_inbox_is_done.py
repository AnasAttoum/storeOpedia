# Generated by Django 4.2 on 2023-07-15 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_inbox'),
    ]

    operations = [
        migrations.AddField(
            model_name='inbox',
            name='is_done',
            field=models.BooleanField(default=0),
        ),
    ]
