# Generated by Django 3.0.8 on 2020-08-18 14:25

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0005_auto_20200818_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='detail',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
