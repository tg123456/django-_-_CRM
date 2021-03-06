# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-30 05:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('stage_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('gender', models.CharField(default='男', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='书名')),
                ('author', models.ManyToManyField(to='app01.Author', verbose_name='作者')),
            ],
            options={
                'verbose_name': '书籍',
                'verbose_name_plural': '书籍',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('display_name', models.CharField(max_length=32)),
                ('phone', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Publish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='出版社名称')),
                ('address', models.CharField(max_length=255, verbose_name='地址')),
                ('phone', models.CharField(max_length=20)),
                ('record_date', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': '出版社',
                'verbose_name_plural': '出版社',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='publish',
            field=models.ForeignKey(default=9999, on_delete=django.db.models.deletion.SET_DEFAULT, to='app01.Publish', verbose_name='出版社'),
        ),
    ]
