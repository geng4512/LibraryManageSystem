from django.contrib import admin
from . import models

admin.site.register(models.READER)
admin.site.register(models.BOOKS)
admin.site.register(models.BORROR)
admin.site.register(models.REVIEW)