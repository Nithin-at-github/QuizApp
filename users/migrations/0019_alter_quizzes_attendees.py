# Generated by Django 4.0.3 on 2022-04-15 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_quizzes_attendees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzes',
            name='attendees',
            field=models.ManyToManyField(blank=True, to='users.users'),
        ),
    ]
