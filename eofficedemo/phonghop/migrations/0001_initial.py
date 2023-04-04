# Generated by Django 4.1.5 on 2023-01-25 14:30

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
            name='PhanQuyen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
                ('qlnhansu', models.ManyToManyField(blank=True, default=None, related_name='qlnhansu', to=settings.AUTH_USER_MODEL)),
                ('qlphonghop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qlphonghop', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LichHop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('time_from', models.TimeField()),
                ('time_end', models.TimeField()),
                ('num_per', models.IntegerField()),
                ('room', models.CharField(choices=[('OPAL', 'OPAL'), ('RUBY', 'RUBY'), ('AMBER', 'AMBER'), ('SAPHIRE', 'SAPHIRE'), ('DIAMOND', 'DIAMOND')], default='RUBY', max_length=15)),
                ('kind', models.CharField(choices=[('Online', 'Online'), ('Offline', 'Offline'), ('Online và Offline', 'Online và Offline')], default='Offline', max_length=50)),
                ('link', models.URLField(blank=True)),
                ('status', models.CharField(choices=[('request', 'Request'), ('waiting', 'Waiting'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('canceled', 'Canceled')], default='request', max_length=15)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('approval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hcns', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phonghop', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GhichuLichHop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, null=True)),
                ('status', models.CharField(max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='phonghop.lichhop')),
            ],
        ),
    ]
