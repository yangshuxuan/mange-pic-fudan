from mangepicfudan import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import urlencode
from pathlib import PurePath,Path
import os

# Create your models here.
    

class Doctor(models.Model):
#   name = models.CharField(max_length=255,verbose_name="医生姓名")
  iddentificationID = models.CharField(max_length=255,unique=True,verbose_name="医生身份证")
#   created_at = models.DateTimeField(auto_now_add=True,verbose_name="医生建档时间")
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  def __str__(self) -> str:
        return f"{self.user.username}-{self.user.first_name}{self.user.last_name}-{self.iddentificationID}"
  class Meta:
        verbose_name = '医生'
        verbose_name_plural = '医生集'

class Patient(models.Model):
  name = models.CharField(max_length=255,verbose_name="病人姓名")
  sex = models.CharField(max_length=255,verbose_name="性别")
  age = models.PositiveSmallIntegerField(blank=True,null=True,verbose_name="年龄")
  iddentificationID = models.CharField(max_length=255,unique=True,verbose_name="病人身份证")
  operateSeqNumber = models.CharField(max_length=255,unique=True,verbose_name="剖验号数")
  deathDate = models.DateField(verbose_name="死亡时日")
  operateDate = models.DateField(verbose_name="解剖时日")
  doctors = models.ManyToManyField(User,verbose_name="剖验医生", related_name='+')
  operateDiagose = models.TextField(verbose_name="解剖诊断")
  deadReason = models.TextField(verbose_name="死亡原因")
  operateRecord = models.FileField(upload_to=settings.records,null=True,verbose_name="解剖记录")
  pptRecord = models.FileField(upload_to=settings.ppt,null=True,verbose_name="PPT")
  otherDocument = models.FileField(upload_to=settings.otherdocs,null=True,verbose_name="其他文档")
  createdAt = models.DateTimeField(auto_now_add=True,verbose_name="患者建档时间")
  lastModifiedAt = models.DateTimeField(auto_now=True,verbose_name="最后修改时间")
  otherDoctors = models.CharField(blank=True,null=True,max_length=255,verbose_name="其他剖验医生")
  sliceNum = models.PositiveSmallIntegerField(blank=True,null=True,verbose_name="切片数")
  creator = models.ForeignKey(User,verbose_name="记录创建者",on_delete=models.PROTECT, related_name='+')
  
  def __init__(self, *args, **kwargs):
            super(Patient, self).__init__(*args, **kwargs)
            self.__original_operateRecord = self.operateRecord
            self.__original_pptRecord = self.pptRecord
            self.__original_otherDocument = self.otherDocument

  def doNeedRename(self):
        return self.__original_operateRecord.name != self.operateRecord.name  or self.__original_pptRecord.name != self.pptRecord.name or self.__original_otherDocument.name != self.otherDocument.name

  def renameFileAfterCreated(self):
      """
      前面已经判断了肯定需要重命名，因此需要save操作
      """
      self.renameFileAfterCreatedGeneral(self.operateRecord,self.__original_operateRecord)
      self.renameFileAfterCreatedGeneral(self.pptRecord,self.__original_pptRecord)
      self.renameFileAfterCreatedGeneral(self.otherDocument,self.__original_otherDocument)
      self.save()


  def renameFileAfterCreatedGeneral(self,p,q):
      
      if p.name != q.name:
            if p:
                  initial_path = p.path
                  initial_name = PurePath(p.name)
                  if initial_name.parent.name != str(self.id):
                        newName = initial_name.parent / str(self.id) / initial_name.name
                        p.name = str(newName)
                        new_path = settings.MEDIA_ROOT / newName
                        new_path.parent.mkdir(parents=True, exist_ok=True)
                        new_path.symlink_to(initial_path)
            q.name = p.name




        
  def __str__(self) -> str:
        return f"{self.name}--{self.iddentificationID}"
  class Meta:
        verbose_name = '病人'
        verbose_name_plural = '病人集'

class  PathologyPictureItem(models.Model):
      pathologyPicture = models.FileField(upload_to=settings.images,verbose_name="病理图片")
      createdAt = models.DateTimeField(auto_now_add=True,verbose_name="图片上传时间")
      patient = models.ForeignKey(Patient, on_delete=models.CASCADE,verbose_name="患者")
      description = models.TextField(blank=True,null=True,verbose_name="图片描述")
      def __init__(self, *args, **kwargs):
            super(PathologyPictureItem, self).__init__(*args, **kwargs)




      class Meta:
            verbose_name = '病理图片'
            verbose_name_plural = '病理图片集'
      def __str__(self) -> str:
            return f"{self.patient.name}的编号为{self.id}的图片"