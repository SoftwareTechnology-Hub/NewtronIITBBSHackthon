# Generated by Django 5.1.3 on 2025-04-04 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elearnapp", "0014_alter_choice_question"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="correct_option",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="question",
            name="option1",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="question",
            name="option2",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="question",
            name="option3",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="question",
            name="option4",
            field=models.CharField(default="", max_length=255),
        ),
    ]
