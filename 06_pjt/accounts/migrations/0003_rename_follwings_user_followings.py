# Generated by Django 3.2.13 on 2023-04-14 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_follwings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='follwings',
            new_name='followings',
        ),
    ]