# Generated by Django 4.1.3 on 2022-11-21 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breddit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='default-avatar.png', upload_to='avatars'),
        ),
    ]
