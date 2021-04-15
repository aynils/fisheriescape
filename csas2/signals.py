import os

from django.db import models
from django.dispatch import receiver
#
# from csas2.models import File
#
#
# @receiver(models.signals.post_delete, sender=File)
# def auto_delete_csas2_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.file:
#         if os.path.isfile(instance.file.path):
#             os.remove(instance.file.path)
#
#
# @receiver(models.signals.pre_save, sender=File)
# def auto_delete_csas2_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False
#
#     try:
#         old_file = File.objects.get(pk=instance.pk).file
#     except File.DoesNotExist:
#         return False
#
#     new_file = instance.file
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)
#


# TODO: add signal to create a person upon creating / updating a user