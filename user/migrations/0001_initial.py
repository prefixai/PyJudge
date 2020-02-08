# Generated by Django 3.0.3 on 2020-02-08 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=256, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('accepted', models.IntegerField(default=0)),
                ('submitted', models.IntegerField(default=0)),
                ('hook', models.URLField(blank=True, null=True)),
                ('hook_times', models.BigIntegerField(blank=True, default=0, null=True)),
                ('nickname', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'profile',
            },
        ),
    ]
