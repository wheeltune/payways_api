# Generated by Django 2.1.1 on 2018-09-19 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_membership_is_admin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='group',
            new_name='room',
        ),
        migrations.RenameField(
            model_name='membership',
            old_name='person',
            new_name='user',
        ),
    ]
