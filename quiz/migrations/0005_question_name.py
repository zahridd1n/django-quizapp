# Generated by Django 5.0.4 on 2024-04-30 16:26

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_remove_question_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='name',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=1),
            preserve_default=False,
        ),
    ]