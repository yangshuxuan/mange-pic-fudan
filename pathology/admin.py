from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html,urlencode
from django.urls import reverse
from django.db.models import Q
from mangepicfudan.settings import STATIC_URL
import os
from . import models
class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.xml'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice
class DeadReasonFilter(InputFilter):
    parameter_name = 'deadReason'
    title = '死亡原因'

    def queryset(self, request, queryset):
        if self.value() is not None:
            deadReason = self.value()

            return queryset.filter(
                Q(deadReason__icontains=deadReason)
            )
class OperateDiagoseFilter(InputFilter):
    parameter_name = 'operateDiagose'
    title = '解剖诊断'

    def queryset(self, request, queryset):
        if self.value() is not None:
            operateDiagose = self.value()

            return queryset.filter(
                Q(operateDiagose__icontains=operateDiagose)
            )
class OperateSeqNumberFilter(InputFilter):
    parameter_name = 'operateSeqNumber'
    title = '剖验号数'

    def queryset(self, request, queryset):
        if self.value() is not None:
            operateSeqNumber = self.value()

            return queryset.filter(
                Q(operateSeqNumber__icontains=operateSeqNumber)
            )
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class DoctorInline(admin.StackedInline):
    model = models.Doctor
    can_delete = False
    verbose_name_plural = '医生集'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (DoctorInline,)
    # search_fields = ['iddentificationID','username','first_name','last_name']

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class PathologyPictureInline(admin.StackedInline):
    model = models.PathologyPictureItem
    extra = 0
@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    # 'doctors',
#       name = models.CharField(max_length=255,verbose_name="病人姓名")
#   sex = models.CharField(max_length=255,verbose_name="性别")
#   age = models.PositiveSmallIntegerField(blank=True,null=True,verbose_name="年龄")
#   iddentificationID = models.CharField(max_length=255,unique=True,verbose_name="病人身份证")
#   operateSeqNumber = models.CharField(max_length=255,unique=True,verbose_name="剖验号数")
#   deathDate = models.DateField(verbose_name="死亡时日")
#   operateDate = models.DateField(verbose_name="解剖时日")
#   doctors = models.ManyToManyField(User,verbose_name="剖验医生", related_name='+')
#   operateDiagose = models.TextField(verbose_name="解剖诊断")
#   deadReason = models.TextField(verbose_name="死亡原因")
#   operateRecord = models.FileField(upload_to=settings.records,null=True,verbose_name="解剖记录")
#   pptRecord = models.FileField(upload_to=settings.ppt,null=True,verbose_name="PPT")
#   otherDocument = models.FileField(upload_to=settings.otherdocs,null=True,verbose_name="其他文档")
#   createdAt = models.DateTimeField(auto_now_add=True,verbose_name="患者建档时间")
#   lastModifiedAt = models.DateTimeField(auto_now=True,verbose_name="最后修改时间")
#   otherDoctors = models.CharField(max_length=255,verbose_name="其他医生")
#   sliceNum = models.PositiveSmallIntegerField(blank=True,null=True,verbose_name="切片数")
#   creator = models.ForeignKey(User,verbose_name="记录创建者",on_delete=models.PROTECT, related_name='+')
    fieldsets = (
        ('患者基本信息', {
            'fields': (('name', 'sex', 'age'), 'iddentificationID','deathDate',),
            # 'classes': ('extrapretty',),
        }),
        ('解剖基本信息', {
            'fields': (('operateSeqNumber', 'operateDate','sliceNum'), 'doctors','otherDoctors',),
            # 'classes': ('extrapretty',),
        }),
        ('解剖结果', {
            'fields': ( 'operateDiagose','deadReason',),
            # 'classes': ('extrapretty',),
        }),
        ('附件', {
            'fields': ( 'operateRecord','pptRecord','otherDocument'),
            # 'classes': ('extrapretty',),
        }),

    )
    filter_horizontal = (
        'doctors',
    )
    list_filter = (
        OperateSeqNumberFilter,
        OperateDiagoseFilter,
        DeadReasonFilter,
    )
    list_display = ['name','sex','age','iddentificationID','operateSeqNumber','deathDate','operateDate','doctorNames','showOperateRecord','showPptRecord','enterPictureList','generateDignoseDoc','creator']
    inlines = [PathologyPictureInline]
    ordering = ['operateSeqNumber','operateDate','deathDate','name','iddentificationID']
    search_fields = ['name','iddentificationID__istartswith','operateSeqNumber','operateDiagose','deadReason']
    # readonly_fields =  ['name','iddentificationID','operateSeqNumber','operateDiagose','deadReason']
    exclude = ('creator',)
    list_per_page = 10
    # autocomplete_fields = ['doctors']
    # raw_id_fields = ['doctors']
    @admin.display(description="诊断报告")
    def generateDignoseDoc(self,patient):
        base_url = "/generatedoc"
        query_string =  urlencode({'patient__id': patient.id})  
        url = '{}?{}'.format(base_url, query_string)
        return format_html('<a href="{}"><img src="{}pathology/explorer.svg" width="25" height="20" alt="浏览"></a>',url,STATIC_URL)
        # return format_html('<a href="{}">{}</a>',url,"浏览")

    @admin.display(description="剖验医生")
    def doctorNames(self,patient):
        return ",".join([ d.username for d in list(patient.doctors.all())])
    @admin.display(description="解剖记录")
    def showOperateRecord(self,patient):
        if patient.operateRecord:
            url = (patient.operateRecord.url 
            + "?" 
            + urlencode({'patient__id':str(patient.id)}))
            return format_html('<a href="{}">{}</a>',url,os.path.basename(patient.operateRecord.name))
        else:
            return None
    # showOperateRecord.allow_tags = True
    @admin.display(description="PPT")
    def showPptRecord(self,patient):
        if patient.pptRecord:
            url = (patient.pptRecord.url 
            + "?" 
            + urlencode({'patient__id':str(patient.id)}))
            return format_html('<a href="{}">{}</a>',url,os.path.basename(patient.pptRecord.name))
        else:
            return None
    
    @admin.display(description="病理图片列表")
    def enterPictureList(self,patient):
        if patient.pathologypictureitem_set.first():
            url = (reverse('admin:pathology_pathologypictureitem_changelist') 
            + "?" 
            + urlencode({'patient__id':str(patient.id)}))
            return format_html('<a href="{}"><img src="{}pathology/finger.svg" width="25" height="20" alt="浏览"></a>',url,STATIC_URL)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "doctors":
            kwargs["queryset"] = User.objects.filter(groups__name='普通医生')
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self,request, obj=None):
        if obj is None:
            return True
        return obj.doctors.filter(id = request.user.id).exists()
    def has_delete_permission(self,request, obj=None):
        if obj is None:
            return True
        return obj.creator.id == request.user.id
        


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
    def has_change_permission(self,request, obj=None):
        if obj is None:
            return True
        return obj.patient.doctors.filter(id = request.user.id).exists()
    def has_delete_permission(self,request, obj=None):
        if obj is None:
            return True
        return obj.patient.doctors.filter(id = request.user.id).exists()
