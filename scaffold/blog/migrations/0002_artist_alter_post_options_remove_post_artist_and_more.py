# Generated by Django 4.2.3 on 2023-08-04 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-date_posted']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='post',
            name='song',
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song', models.FileField(blank=True, null=True, upload_to='')),
                ('composer', models.CharField(blank=True, max_length=100, null=True)),
                ('artist', models.ManyToManyField(blank=True, null=True, to='blog.artist')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='artist',
            field=models.ManyToManyField(blank=True, null=True, to='blog.artist'),
        ),
        migrations.AddField(
            model_name='post',
            name='song',
            field=models.ManyToManyField(blank=True, null=True, to='blog.song'),
        ),
    ]
