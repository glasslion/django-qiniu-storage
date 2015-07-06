from django.db import models
from django.contrib import admin


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/%d')

class Attachment(models.Model):
    attachment = models.FileField()


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass
