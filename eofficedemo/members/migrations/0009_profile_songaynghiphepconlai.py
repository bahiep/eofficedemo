# Generated by Django 4.1.5 on 2023-02-19 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_profile_songaynghikhongphep_profile_songaynghiphep_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='songaynghiphepconlai',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
