# Generated by Django 5.1.3 on 2025-04-04 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elearnapp", "0013_alter_quiz_time_limit_alter_quiz_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="choice",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="elearnapp.question"
            ),
        ),
    ]
