from django.contrib import admin
from django.utils.html import format_html,urlencode
from django.urls import reverse
import os
from . import models
# Register your models here.
@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    
    list_display = ['id','iddentificationID','name','created_at']
    # list_editable = ['iddentificationID','name']
    ordering = ['created_at','name']
    search_fields = ['name__istartswith','iddentificationID__istartswith']
    list_per_page = 10
    

class PathologyPictureInline(admin.StackedInline):
    model = models.PathologyPictureItem
    extra = 0
@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    # 'doctors',
    list_display = ['name','sex','iddentificationID','operateSeqNumber','deathDate','operateDate','doctorNames','showOperateRecord','showPptRecord','enterPictureList']
    inlines = [PathologyPictureInline]
    ordering = ['operateSeqNumber','operateDate','deathDate','name','iddentificationID']
    search_fields = ['name','iddentificationID__istartswith','operateSeqNumber','operateDiagose','deadReason']
    readonly_fields =  ['name','iddentificationID','operateSeqNumber','operateDiagose','deadReason']
    list_per_page = 10
    autocomplete_fields = ['doctors']

    @admin.display(description="剖验医生")
    def doctorNames(self,patient):
        return ",".join([ d.name for d in list(patient.doctors.all())])
    @admin.display(description="解剖记录")
    def showOperateRecord(self,patient):
        if patient.operateRecord:
            return format_html('<a href="{}">{}</a>',patient.operateRecord.url,os.path.basename(patient.operateRecord.name))
        else:
            return None
    @admin.display(description="纠纷PPT")
    def showPptRecord(self,patient):
        if patient.pptRecord:
            return format_html('<a href="{}">{}</a>',patient.pptRecord.url,os.path.basename(patient.pptRecord.name))
        else:
            return None
    
    @admin.display(description="病理图片列表")
    def enterPictureList(self,patient):
        if patient.pathologypictureitem_set.first():
            url = (reverse('admin:pathology_pathologypictureitem_changelist') 
            + "?" 
            + urlencode({'patient__id':str(patient.id)}))
            return format_html('<a href="{}"><img src="/media/icons/finger.svg" width="25" height="20" alt="浏览"></a>',url)


@admin.register(models.PathologyPictureItem)
class PathologyPictureAdmin(admin.ModelAdmin):
    
    list_display = ['patient','createdAt','showPathologyPicture']
    autocomplete_fields = ['patient']
    ordering = ['createdAt']
    list_per_page = 10
    @admin.display(description="病理图片")
    def showPathologyPicture(self,pathologyPictureItem):
        if pathologyPictureItem.pathologyPicture:
            return format_html('<a href="{}">{}</a>',pathologyPictureItem.pathologyPicture.url,os.path.basename(pathologyPictureItem.pathologyPicture.name))
        else:
            return None
