# Generated by Django 4.2.3 on 2023-08-07 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metaversemusic', '0003_alter_artist_artist_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='uploaded_by',
        ),
        migrations.RemoveField(
            model_name='song',
            name='artist',
        ),
        migrations.AddField(
            model_name='song',
            name='artist',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]