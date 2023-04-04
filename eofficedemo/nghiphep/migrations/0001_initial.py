# Generated by Django 4.1.5 on 2023-01-20 01:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Nghỉ phép', 'Nghỉ phép'), ('Nghỉ ốm', 'Nghỉ ốm'), ('Nghỉ sanh', 'Nghỉ sanh'), ('Nghỉ hôn nhân', 'Nghỉ hôn nhân'), ('Nghỉ tang lễ', 'Nghỉ tang lễ'), ('Nghỉ khác', 'Nghỉ khác')], default='Nghỉ phép', max_length=100)),
                ('date_from', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('numday', models.FloatField()),
                ('body', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('like_count', models.BigIntegerField(default='0')),
                ('status', models.CharField(choices=[('request', 'Request'), ('waiting', 'Waiting'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='request', max_length=10)),
                ('approval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager', to=settings.AUTH_USER_MODEL)),
                ('approvalbod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, default=None, related_name='like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]