# Generated by Django 2.0 on 2018-02-07 09:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('erpp_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='appmaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('am_name', models.CharField(default=True, max_length=100)),
                ('am_type', models.CharField(choices=[('MN', 'MENU'), ('FRM', 'FORM')], max_length=5)),
                ('am_level', models.SmallIntegerField()),
                ('am_group', models.CharField(choices=[('GRP', 'Group'), ('NGRP', 'Not Group')], max_length=5)),
                ('am_isactive', models.BooleanField(default=True)),
                ('am_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('am_creater', models.CharField(default=True, max_length=100)),
                ('am_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('am_updater', models.CharField(default=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='appmasterform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amf_name', models.CharField(default=django.utils.timezone.now, max_length=100)),
                ('amf_filenamehtml', models.CharField(default=django.utils.timezone.now, max_length=100)),
                ('amf_isactive', models.BooleanField(default=True)),
                ('amf_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('amf_creater', models.CharField(default=True, max_length=100)),
                ('amf_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('amf_updater', models.CharField(default=True, max_length=100)),
                ('amf_appmaster', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='erpp_dasboard.appmaster')),
            ],
        ),
        migrations.CreateModel(
            name='appmasterpermissionform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ampf_isnew', models.BooleanField(default=True)),
                ('ampf_isselect', models.BooleanField(default=True)),
                ('ampf_isinsert', models.BooleanField(default=True)),
                ('ampf_isupdate', models.BooleanField(default=True)),
                ('ampf_isdelete', models.BooleanField(default=True)),
                ('ampf_isprint', models.BooleanField(default=True)),
                ('ampf_isexport', models.BooleanField(default=True)),
                ('ampf_isimport', models.BooleanField(default=True)),
                ('ampf_isactive', models.BooleanField(default=True)),
                ('ampf_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('ampf_creater', models.CharField(default=True, max_length=100)),
                ('ampf_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('ampf_updater', models.CharField(default=True, max_length=100)),
                ('ampf_appmasterform', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='erpp_dasboard.appmasterform')),
                ('ampf_useraccount', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='erpp_auth.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='appmasterstructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ams_appmaster_child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ams_appmaster_child', to='erpp_dasboard.appmaster')),
                ('ams_appmaster_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ams_appmaster_parent', to='erpp_dasboard.appmaster')),
            ],
        ),
    ]
