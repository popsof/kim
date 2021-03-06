# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 23:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FaceFriend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('face_id', models.CharField(max_length=32)),
                ('face_name', models.CharField(max_length=100)),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FaceRanking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('comment', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='facefriend',
            name='face_ranking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sns.FaceRanking'),
        ),
    ]
