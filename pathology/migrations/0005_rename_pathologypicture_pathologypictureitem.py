# Generated by Django 3.2.5 on 2021-09-08 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pathology', '0004_auto_20210908_1027'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PathologyPicture',
            new_name='PathologyPictureItem',
        ),
    ]