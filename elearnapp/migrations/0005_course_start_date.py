# Generated by Django 5.1.3 on 2025-04-04 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elearnapp", "0004_announcement"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
