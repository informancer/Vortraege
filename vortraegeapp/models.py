from django.db import models

# Supporting functions
def pressetext_upload_to(instance, filename):
    return 'pressetext-%s'%instance.datum.strftime('%Y%m%d')
def aushang_upload_to(instance, filename):
    return 'aushang-%s'%instance.datum.strftime('%Y%m%d')
def flyer_upload_to(instance, filename):
    return 'flyer-%s'%instance.datum.strftime('%Y%m%d')

# Create your models here.
class Vortrag(models.Model):
    datum = models.DateTimeField() 
    thema = models.CharField(max_length=200)
    referent = models.CharField(max_length=200)
    orgapate = models.CharField(max_length=200, blank=True)
    beschreibung = models.TextField(blank=True)
    pressetext = models.FileField(upload_to=pressetext_upload_to, blank=True)
    aushang = models.FileField(upload_to=aushang_upload_to, blank=True)
    flyer = models.FileField(upload_to=flyer_upload_to, blank=True)
    folien = models.URLField(blank=True)
    audio = models.URLField(blank=True)

    def __unicode__(self):
        return self.thema
