# Generated by Django 3.1.2 on 2020-10-27 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20201027_0931'),
    ]

    operations = [
        migrations.RenameField(
            model_name='name',
            old_name='schedule',
            new_name='scheduled_date',
        ),
    ]
