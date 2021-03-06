# Generated by Django 2.0 on 2018-02-07 09:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='useraccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ua_username', models.CharField(max_length=100, unique=True)),
                ('ua_userpassword', models.CharField(default=True, max_length=100)),
                ('ua_isactive', models.BooleanField(default=False)),
                ('ua_keystone_id', models.IntegerField(default=True, null=True)),
                ('ua_keystone_user_id', models.CharField(default=True, max_length=50, null=True)),
                ('ua_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('ua_creater', models.CharField(default=True, max_length=100)),
                ('ua_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('ua_updater', models.CharField(default=True, max_length=100)),
                ('ua_issuspend', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='userfotoprofile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ufp_name', models.CharField(max_length=100, null=True)),
                ('ufp_status', models.CharField(max_length=100, null=True)),
                ('ufp_note', models.CharField(max_length=100, null=True)),
                ('ufp_path', models.CharField(max_length=100, null=True)),
                ('ufp_filename', models.CharField(max_length=100, null=True)),
                ('ufp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('ufp_creater', models.CharField(default=True, max_length=100)),
                ('ufp_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('ufp_updater', models.CharField(default=True, max_length=100)),
                ('ufp_useraccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erpp_auth.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='userprofile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up_name', models.CharField(default=True, max_length=255)),
                ('up_birthplace', models.CharField(default=True, max_length=100)),
                ('up_birthdate', models.DateField()),
                ('up_gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('up_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('up_creater', models.CharField(default=True, max_length=100)),
                ('up_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('up_updater', models.CharField(default=True, max_length=100)),
                ('up_useraccount', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='erpp_auth.useraccount')),
            ],
        ),
    ]
