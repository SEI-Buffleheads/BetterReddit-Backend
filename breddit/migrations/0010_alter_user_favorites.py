# Generated by Django 4.1.3 on 2022-11-26 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breddit', '0009_alter_post_link_alter_user_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorited', to='breddit.post'),
        ),
    ]
