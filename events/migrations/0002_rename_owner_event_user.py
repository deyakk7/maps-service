# Generated by Django 4.2.5 on 2023-11-27 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='owner',
            new_name='user',
        ),
    ]
