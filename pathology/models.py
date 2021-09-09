from django.db import models

# Create your models here.
    

class Doctor(models.Model):
  name = models.CharField(max_length=255,verbose_name="医生姓名")
  iddentificationID = models.CharField(max_length=255,unique=True,verbose_name="医生身份证")
  created_at = models.DateTimeField(auto_now_add=True,verbose_name="医生建档时间")
  def __str__(self) -> str:
        return f"{self.name}-{self.iddentificationID}"
  class Meta:
        verbose_name = '医生'
        verbose_name_plural = '医生集'

class Patient(models.Model):
  name = models.CharField(max_length=255,verbose_name="病人姓名")
  sex = models.CharField(max_length=255,verbose_name="性别")
  iddentificationID = models.CharField(max_length=255,unique=True,verbose_name="病人身份证")
  operateSeqNumber = models.CharField(max_length=255,unique=True,verbose_name="剖验号数")
  deathDate = models.DateField(verbose_name="死亡时日")
  operateDate = models.DateField(verbose_name="解剖时日")
  doctors = models.ManyToManyField(Doctor,verbose_name="剖验医生", related_name='+')
  operateDiagose = models.TextField(verbose_name="解剖诊断")
  deadReason = models.TextField(verbose_name="死亡原因")
  operateRecord = models.FileField(upload_to='records',null=True,verbose_name="解剖记录")
  pptRecord = models.FileField(upload_to='ppt',null=True,verbose_name="纠纷PPT")
  def __str__(self) -> str:
        return f"{self.name}"
  class Meta:
        verbose_name = '病人'
        verbose_name_plural = '病人集'

class  PathologyPictureItem(models.Model):
    pathologyPicture = models.FileField(upload_to='images',verbose_name="病理图片")
    createdAt = models.DateTimeField(auto_now_add=True,verbose_name="图片上传时间")
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT,verbose_name="患者")
    class Meta:
        verbose_name = '病理图片'
        verbose_name_plural = '病理图片集'
    def __str__(self) -> str:
        return f"{self.patient.name}第{self.id}张图片"