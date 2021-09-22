from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Patient,PathologyPictureItem
@receiver(post_save,sender=Patient)
def renameFileAfterCreated(sender,instance,created,raw,using,update_fields,**kwargs):
    if instance.doNeedRename():
        instance.renameFileAfterCreated()