# Generated by Django 4.2.3 on 2023-08-07 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_country_profile_user_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.CharField(default='Aug 29 1985', max_length=20),
        ),
    ]