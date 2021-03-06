from django.db import models

# Supporting functions
def presstext_upload_to(instance, filename):
    return 'pressetext-%s.txt'%instance.start.strftime('%Y%m%d')
def poster_upload_to(instance, filename):
    return 'aushang-%s.pdf'%instance.start.strftime('%Y%m%d')
def flyer_upload_to(instance, filename):
    return 'flyer-%s.pdf'%instance.start.strftime('%Y%m%d')

# Create your models here.
class Event(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    url =  models.URLField(blank=True)

    def __unicode__(self):
        return self.title

class Talk(models.Model):
    start = models.DateTimeField() 
    title = models.CharField(max_length=200)
    speaker = models.CharField(max_length=200)
    organiser = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    presstext = models.FileField(upload_to=presstext_upload_to, blank=True)
    poster = models.FileField(upload_to=poster_upload_to, blank=True)
    flyer = models.FileField(upload_to=flyer_upload_to, blank=True)
    slides = models.URLField(blank=True)
    audio = models.URLField(blank=True)
    event = models.ManyToManyField(Event)

    def __unicode__(self):
        return self.title
