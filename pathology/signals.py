from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Patient,PathologyPictureItem
@receiver(post_save,sender=Patient)
def renameFileAfterCreated(sender,instance,created,raw,using,update_fields,**kwargs):
    if created or instance.doNeedRename():
        instance.renameFileAfterCreated()

@receiver(post_delete, sender=Patient)
def deleteFileAfterRecordDel(sender,instance,using,**kwargs):
    instance.cleanFile()


@receiver(post_save,sender=PathologyPictureItem)
def renameFileAfterCreated(sender,instance,created,raw,using,update_fields,**kwargs):
    instance.deleteFileAfterChange()

@receiver(post_delete, sender=PathologyPictureItem)
def deleteFileAfterRecordDel(sender,instance,using,**kwargs):
    instance.cleanFile()