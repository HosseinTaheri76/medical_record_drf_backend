from .models import Visit, Document
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete


@receiver(pre_save, sender=Visit)
def set_doctor_name(sender, instance, **kwargs):
    if instance.doctor:
        instance.doctor_name = instance.doctor.name


@receiver(pre_delete, sender=Visit)
@receiver(pre_delete, sender=Document)
def delete_associated_files(sender, instance, **kwargs):
    instance.file.delete()
