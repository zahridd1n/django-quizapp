# Generated by Django 5.0.4 on 2024-05-01 11:34

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_alter_question_name_alter_quiz_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='name',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
