# Generated by Django 4.0.3 on 2022-03-18 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quizzes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Quiz Title')),
                ('tot_questions', models.IntegerField()),
                ('max_time', models.IntegerField()),
                ('max_mark', models.IntegerField()),
                ('date_added', models.DateTimeField(verbose_name='Date Added')),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('max_mark', models.IntegerField()),
                ('tot_questions', models.IntegerField()),
                ('correct_answers', models.IntegerField()),
                ('wrong_answers', models.IntegerField()),
                ('date', models.DateTimeField(verbose_name='Date Attended')),
                ('quiz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.quizzes')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('mark_correct', models.FloatField()),
                ('mark_wrong', models.FloatField()),
                ('quiz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.quizzes')),
            ],
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200, verbose_name='Option Value')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.questions')),
            ],
        ),
    ]
