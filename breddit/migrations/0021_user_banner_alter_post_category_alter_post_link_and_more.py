# Generated by Django 4.1.3 on 2022-11-28 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breddit', '0020_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='banner',
            field=models.ImageField(default='banner.jpg', upload_to='banners'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(default='random', max_length=256),
        ),
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.URLField(blank=True, default='https://www.google.com/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=256),
        ),
    ]
