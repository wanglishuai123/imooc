# Generated by Django 2.2.5 on 2020-01-28 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_classics',
            field=models.BooleanField(default=False, verbose_name='经典课程'),
        ),
    ]
