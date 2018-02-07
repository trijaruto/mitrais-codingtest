from django.db import models
from django.db import models
from django.utils import timezone
from erpp_auth.models import useraccount

# Create your models here.
class appmaster(models.Model):
    TYPE = (('MN','MENU'),('FRM','FORM'))
    GROUP = (('GRP','Group'),('NGRP','Not Group'))
    am_name = models.CharField(max_length=100, default=True)
    am_type = models.CharField(max_length=5, choices=TYPE)
    am_level = models.SmallIntegerField()
    am_group = models.CharField(max_length=5, choices=GROUP)
    am_isactive = models.BooleanField(default=True)
    am_created = models.DateTimeField(default=timezone.now)
    am_creater = models.CharField(max_length=100, default=True)
    am_updated = models.DateTimeField(default=timezone.now)
    am_updater = models.CharField(max_length=100, default=True)

class appmasterstructure(models.Model):
    ams_appmaster_parent = models.ForeignKey(appmaster, related_name='ams_appmaster_parent', on_delete=models.CASCADE)
    ams_appmaster_child = models.ForeignKey(appmaster, related_name='ams_appmaster_child', on_delete=models.CASCADE)

class appmasterform(models.Model):
    amf_appmaster = models.OneToOneField(appmaster, on_delete=models.CASCADE)
    amf_name = models.CharField(max_length=100, default=timezone.now)
    amf_filenamehtml = models.CharField(max_length=100, default=timezone.now)
    amf_isactive = models.BooleanField(default=True)
    amf_created = models.DateTimeField(default=timezone.now)
    amf_creater = models.CharField(max_length=100, default=True)
    amf_updated = models.DateTimeField(default=timezone.now)
    amf_updater = models.CharField(max_length=100, default=True)

class appmasterpermissionform(models.Model):
    ampf_useraccount = models.OneToOneField(useraccount, on_delete=models.CASCADE)
    ampf_appmasterform = models.OneToOneField(appmasterform, on_delete=models.CASCADE)
    ampf_isnew = models.BooleanField(default=True)
    ampf_isselect = models.BooleanField(default=True)
    ampf_isinsert = models.BooleanField(default=True)
    ampf_isupdate = models.BooleanField(default=True)
    ampf_isdelete = models.BooleanField(default=True)
    ampf_isprint = models.BooleanField(default=True)
    ampf_isexport = models.BooleanField(default=True)
    ampf_isimport = models.BooleanField(default=True)
    ampf_isactive = models.BooleanField(default=True)
    ampf_created = models.DateTimeField(default=timezone.now)
    ampf_creater = models.CharField(max_length=100, default=True)
    ampf_updated = models.DateTimeField(default=timezone.now)
    ampf_updater = models.CharField(max_length=100, default=True)
