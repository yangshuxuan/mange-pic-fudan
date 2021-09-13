from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import Patient
@receiver(post_save,sender=Patient)
def renameFileAfterCreated(sender,instance,created,raw,using,update_fields,**kwargs):
    if created or instance.doNeedRename():
        instance.renameFileAfterCreated()

# @receiver(pre_save, sender=Patient)
# def renameFileBeforeChange(sender,instance, raw,using,update_fields,**kwargs):
#     if instance.id is None:
#         return
#     else:
#         instance.renameFileBeforeChange()
