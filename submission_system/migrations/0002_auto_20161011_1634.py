# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-11 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courser',
            options={'verbose_name': '课程', 'verbose_name_plural': '课程'},
        ),
        migrations.AlterModelOptions(
            name='homework',
            options={'verbose_name': '作业', 'verbose_name_plural': '作业'},
        ),
        migrations.AlterModelOptions(
            name='homeworkanswer',
            options={'verbose_name': '提交的作业', 'verbose_name_plural': '提交的作业'},
        ),
        migrations.AddField(
            model_name='homeworkanswer',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='上传的图'),
        ),
    ]