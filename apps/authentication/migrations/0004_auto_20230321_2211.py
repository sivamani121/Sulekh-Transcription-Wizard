# Generated by Django 3.2.6 on 2023-03-21 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20230321_2115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='password1',
            new_name='password',
        ),
        migrations.RemoveField(
            model_name='users',
            name='mobileno',
        ),
        migrations.RemoveField(
            model_name='users',
            name='password2',
        ),
    ]
