from django.db import models

# Create your models here.
    

class Doctor(models.Model):
  name = models.CharField(max_length=255,verbose_name="医生姓名")
  iddentificationID = models.CharField(max_length=255,unique=True,verbose_name="医生身份证")
  created_at = models.DateTimeField(auto_now_add=True,verbose_name="医生建档时间")
  class Meta:
        verbose_name = '医生'
        verbose_name_plural = '医生集'