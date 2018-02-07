from django.db import models
from django.utils import timezone
from _erpp_authadmin.models import useraccountadmin

# Create your models here.
class appmasteradmin(models.Model):
    TYPE = (('ROT','ROOT'),('MN','MENU'),('FRM','FORM'))
    ama_name = models.CharField(max_length=100, default=True)
    ama_type = models.CharField(max_length=5, choices=TYPE)
    ama_level = models.SmallIntegerField()
    ama_isgroup = models.BooleanField(default=False)
    ama_isactive = models.BooleanField(default=True)
    ama_created = models.DateTimeField(default=timezone.now)
    ama_creater = models.CharField(max_length=100, default=True)
    ama_updated = models.DateTimeField(default=timezone.now)
    ama_updater = models.CharField(max_length=100, default=True)

class appmasteradminstructure(models.Model):
    amas_appmasteradmin_parent = models.ForeignKey(appmasteradmin, related_name='amas_appmasteradmin_parent', on_delete=models.CASCADE)
    amas_appmasteradmin_child = models.ForeignKey(appmasteradmin, related_name='amas_appmasteradmin_child', on_delete=models.CASCADE)

class appmasteradminform(models.Model):
    amaf_appmasteradmin = models.OneToOneField(appmasteradmin, on_delete=models.CASCADE)
    amaf_name = models.CharField(max_length=100, default=True)
    amaf_filenamehtml = models.CharField(max_length=100, default=True)
    amaf_isactive = models.BooleanField(default=True)
    amaf_created = models.DateTimeField(default=timezone.now)
    amaf_creater = models.CharField(max_length=100, default=True)
    amaf_updated = models.DateTimeField(default=timezone.now)
    amaf_updater = models.CharField(max_length=100, default=True)

class appmasteradminpermissionform(models.Model):
    amapf_useraccountadmin = models.OneToOneField(useraccountadmin, on_delete=models.CASCADE)
    amapf_appmasteradminform = models.OneToOneField(appmasteradminform, on_delete=models.CASCADE)
    amapf_isnew = models.BooleanField(default=True)
    amapf_isselect = models.BooleanField(default=True)
    amapf_isinsert = models.BooleanField(default=True)
    amapf_isupdate = models.BooleanField(default=True)
    amapf_isdelete = models.BooleanField(default=True)
    amapf_isprint = models.BooleanField(default=True)
    amapf_isexport = models.BooleanField(default=True)
    amapf_isimport = models.BooleanField(default=True)
    amapf_isactive = models.BooleanField(default=True)
    amapf_created = models.DateTimeField(default=timezone.now)
    amapf_creater = models.CharField(max_length=100, default=True)
    amapf_updated = models.DateTimeField(default=timezone.now)
    amapf_updater = models.CharField(max_length=100, default=True)

