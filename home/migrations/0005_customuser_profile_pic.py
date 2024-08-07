# Generated by Django 5.0.6 on 2024-06-25 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_customuser_genre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(blank=True, default='/media/profile_img/standard.png', upload_to='profile_img/', verbose_name='Profile Picture'),
        ),
    ]
