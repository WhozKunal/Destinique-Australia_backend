# Generated by Django 4.2.4 on 2024-08-09 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0029_registereduser_is_profile_complete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registereduser',
            old_name='is_profile_complete',
            new_name='is_verified',
        ),
    ]
