# Generated by Django 4.1.5 on 2023-01-20 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phongban',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='members.department'),
        ),
    ]