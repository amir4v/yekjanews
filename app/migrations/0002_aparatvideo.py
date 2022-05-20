# Generated by Django 3.2 on 2022-05-20 10:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AparatVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('media', models.CharField(db_index=True, max_length=2048, unique=True)),
            ],
        ),
    ]
