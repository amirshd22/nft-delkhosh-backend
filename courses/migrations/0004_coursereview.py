# Generated by Django 3.2.5 on 2022-03-17 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0003_course_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseReview',
            fields=[
                ('rate', models.IntegerField(blank=True, default=0, null=True)),
                ('content', models.CharField(max_length=255, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='review_course', to='courses.course')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
