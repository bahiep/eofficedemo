# Generated by Django 4.1.7 on 2023-02-23 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phonghop', '0003_alter_lichhop_room'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lichhop',
            name='link',
        ),
    ]
