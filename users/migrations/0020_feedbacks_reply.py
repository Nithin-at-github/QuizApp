# Generated by Django 4.0.3 on 2022-04-18 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_quizzes_attendees'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbacks',
            name='reply',
            field=models.TextField(blank=True),
        ),
    ]
