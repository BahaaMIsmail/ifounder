# Generated by Django 5.0.4 on 2024-05-06 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_rename_exam_question_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='qdubl',
            name='source',
            field=models.CharField(max_length=400, null=True),
        ),
    ]
