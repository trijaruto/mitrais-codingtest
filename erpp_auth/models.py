from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

# Create your models here.
class useraccount(models.Model):
    ua_username = models.CharField(max_length=100, unique=True)
    ua_userpassword = models.CharField(max_length=100, default=True)
    ua_isactive = models.BooleanField(default=False)
    ua_keystone_id = models.IntegerField(default=True, null=True)
    ua_keystone_user_id = models.CharField(max_length=50, default=True, null=True)
    ua_created = models.DateTimeField(default=timezone.now)
    ua_creater = models.CharField(max_length=100, default=True)
    ua_updated = models.DateTimeField(default=timezone.now)
    ua_updater = models.CharField(max_length=100, default=True)
    ua_issuspend = models.BooleanField(default=False)

class userprofile(models.Model):
    GENDER = (('M','Male'),('F','Female'),)
    up_useraccount = models.OneToOneField(useraccount, on_delete=models.CASCADE)
    up_name = models.CharField(max_length=255, default=True)
    up_birthplace = models.CharField(max_length=100, default=True)
    up_birthdate = models.DateField()
    up_gender = models.CharField(max_length=1, choices=GENDER)
    up_created = models.DateTimeField(default=timezone.now)
    up_creater = models.CharField(max_length=100, default=True)
    up_updated = models.DateTimeField(default=timezone.now)
    up_updater = models.CharField(max_length=100, default=True)

class userfotoprofile(models.Model):
    ufp_useraccount = models.ForeignKey(useraccount, on_delete=models.CASCADE)
    ufp_name = models.CharField(max_length=100, null=True)
    ufp_status = models.CharField(max_length=100, null=True)
    ufp_note = models.CharField(max_length=100, null=True)
    ufp_path = models.CharField(max_length=100, null=True)
    ufp_filename = models.CharField(max_length=100, null=True)
    ufp_created = models.DateTimeField(default=timezone.now)
    ufp_creater = models.CharField(max_length=100, default=True)
    ufp_updated = models.DateTimeField(default=timezone.now)
    ufp_updater = models.CharField(max_length=100, default=True)
