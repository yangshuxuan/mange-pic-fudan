# Generated by Django 3.2.5 on 2021-09-07 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathology', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='病人姓名')),
                ('sex', models.CharField(max_length=255, verbose_name='性别')),
                ('iddentificationID', models.CharField(max_length=255, unique=True, verbose_name='病人身份证')),
                ('operateSeqNumber', models.CharField(max_length=255, unique=True, verbose_name='剖验号数')),
                ('deathDate', models.DateField(verbose_name='死亡时日')),
                ('operateDate', models.DateField(verbose_name='解剖时日')),
                ('operateDiagose', models.TextField(verbose_name='解剖诊断')),
                ('deadReason', models.TextField(verbose_name='死亡原因')),
                ('doctors', models.ManyToManyField(related_name='_pathology_patient_doctors_+', to='pathology.Doctor', verbose_name='剖验医生')),
            ],
            options={
                'verbose_name': '病人',
                'verbose_name_plural': '病人集',
            },
        ),
    ]
