# Generated by Django 4.2.3 on 2023-08-26 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_date_of_birth'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('artist', 'Artist'), ('fan', 'Fan')], default='fan', max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user_type',
        ),
    ]