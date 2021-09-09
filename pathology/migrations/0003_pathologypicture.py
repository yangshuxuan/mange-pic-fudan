# Generated by Django 3.2.5 on 2021-09-07 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pathology', '0002_patient'),
    ]

    operations = [
        migrations.CreateModel(
            name='PathologyPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pathologyPicture', models.FileField(upload_to='images', verbose_name='病理图片')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='图片上传时间')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pathology.patient', verbose_name='患者')),
            ],
            options={
                'verbose_name': '病理图片',
                'verbose_name_plural': '病理图片集',
            },
        ),
    ]