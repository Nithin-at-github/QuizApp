# Generated by Django 4.0.3 on 2022-03-31 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_quizzes_attendees'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='password',
        ),
    ]
