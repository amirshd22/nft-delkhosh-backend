# Generated by Django 3.2.5 on 2022-03-26 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_coursereview'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercourses',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
