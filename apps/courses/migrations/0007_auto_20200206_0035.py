# Generated by Django 2.2.5 on 2020-02-06 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_notice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.CharField(max_length=1000, verbose_name='访问链接'),
        ),
    ]
