# Generated by Django 5.0.4 on 2024-04-30 16:10

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_alter_question_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='name',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
