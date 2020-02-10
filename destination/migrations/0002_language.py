# Generated by Django 3.0.3 on 2020-02-10 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('destination', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20)),
                ('display', models.CharField(max_length=40)),
                ('enable', models.BooleanField(default=True)),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='destination.Platform')),
            ],
            options={
                'db_table': 'language',
            },
        ),
    ]
