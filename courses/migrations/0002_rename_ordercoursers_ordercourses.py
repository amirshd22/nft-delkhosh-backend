# Generated by Django 3.2.5 on 2022-02-23 19:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderCoursers',
            new_name='OrderCourses',
        ),
    ]
