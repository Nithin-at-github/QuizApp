# Generated by Django 4.0.3 on 2022-03-23 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_answers_option_id_answers_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='answer',
            field=models.CharField(choices=[('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3'), ('option4', 'Option 4')], default='Select', max_length=200),
        ),
        migrations.DeleteModel(
            name='Answers',
        ),
    ]
