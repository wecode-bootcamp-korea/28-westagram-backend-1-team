# Generated by Django 3.2.9 on 2021-12-17 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=300)),
                ('mobile_number', models.CharField(max_length=20, unique=True)),
                ('other_info', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
