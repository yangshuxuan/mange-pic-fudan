# Generated by Django 3.2.5 on 2021-11-30 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathology', '0006_delete_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathologypictureitem',
            name='pathologyPicture',
            field=models.ImageField(upload_to='images', verbose_name='病理图片'),
        ),
    ]
