# Generated by Django 4.2.3 on 2023-08-26 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_usertype_remove_profile_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_artist',
            field=models.BooleanField(default=False),
        ),
    ]