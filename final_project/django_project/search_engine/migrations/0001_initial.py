# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 17:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('image_url', models.URLField()),
                ('rank', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('scheduler', 'scheduler'), ('done', 'done')], default='scheduler', max_length=10)),
                ('quantity_images', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search_engine.Task'),
        ),
    ]
