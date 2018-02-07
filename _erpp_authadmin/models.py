from django.db import models
from django.utils import timezone

# Create your models here.
class usertypeadmin(models.Model):
    uta_name = models.CharField(max_length=100, unique=True, default=True)
    uta_created = models.DateTimeField(default=timezone.now)
    uta_creater = models.CharField(max_length=100, default=True)
    uta_updated = models.DateTimeField(default=timezone.now)
    uta_updater = models.CharField(max_length=100, default=True)

class useraccountadmin(models.Model):
    uaa_username = models.CharField(max_length=100, unique=True)
    uaa_userpassword = models.CharField(max_length=100, default=True)
    uaa_usertypeadmin = models.ForeignKey(usertypeadmin, on_delete=models.CASCADE)
    uaa_isactive = models.BooleanField(default=False)
    uaa_keystone_id = models.IntegerField(default=True, null=True)
    uaa_keystone_user_id = models.CharField(max_length=50, default=True, null=True)
    uaa_created = models.DateTimeField(default=timezone.now)
    uaa_creater = models.CharField(max_length=100, default=True)
    uaa_updated = models.DateTimeField(default=timezone.now)
    uaa_updater = models.CharField(max_length=100, default=True)
    uaa_issuspend = models.BooleanField(default=False)

class userprofileadmin(models.Model):
    GENDER = (('M','Male'),('F','Female'),)
    upa_useraccountadmin = models.OneToOneField(useraccountadmin, on_delete=models.CASCADE)
    upa_name = models.CharField(max_length=100, default=True)
    upa_birthplace = models.CharField(max_length=100, default=True)
    upa_birthdate = models.DateField()
    upa_gender = models.CharField(max_length=1, choices=GENDER)
    upa_created = models.DateTimeField(default=timezone.now)
    upa_creater = models.CharField(max_length=100, default=True)
    upa_updated = models.DateTimeField(default=timezone.now)
    upa_updater = models.CharField(max_length=100, default=True)

class userfotoprofileadmin(models.Model):
    ufpa_useraccountadmin = models.ForeignKey(useraccountadmin, on_delete=models.CASCADE)
    ufpa_name = models.CharField(max_length=100, default=True)
    ufpa_status = models.CharField(max_length=100, default=True)
    ufpa_note = models.CharField(max_length=100, default=True)
    ufpa_path = models.CharField(max_length=100, default=True)
    ufpa_filename = models.CharField(max_length=100, default=True)
    ufpa_created = models.DateTimeField(default=timezone.now)
    ufpa_creater = models.CharField(max_length=100, default=True)
    ufpa_updated = models.DateTimeField(default=timezone.now)
    ufpa_updater = models.CharField(max_length=100, default=True)
