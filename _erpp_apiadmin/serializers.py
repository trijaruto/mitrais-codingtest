from django.contrib.auth.models import User
from _erpp_authadmin.models import useraccountadmin, usertypeadmin
from _erpp_dasboardadmin.models import appmasteradmin
from rest_framework import serializers

# USER FOR DJANGO RESTFRAMEWORK
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'is_superuser', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'last_login')#, 'snippets')

# USERTYPEADMIN
class UserTypeAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = usertypeadmin
        fields = ('url', 'id', 'uta_name', 'uta_created', 'uta_creater', 'uta_updated', 'uta_updater')

# USERACCOUNTADMIN
class UserAccountAdminSerializer(serializers.HyperlinkedModelSerializer):
    uaa_usertypeadmin = serializers.ReadOnlyField(source='uaa_usertypeadmin.uta_name')
    class Meta:
        model = useraccountadmin
        fields = ('url', 'id', 'uaa_username', 'uaa_userpassword', 'uaa_usertypeadmin', 'uaa_isactive', 'uaa_keystone_id', 'uaa_keystone_user_id', 'uaa_created', 'uaa_creater', 'uaa_updated', 'uaa_updater', 'uaa_issuspend')

# APPMASTERADMIN
class AppMasterAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = appmasteradmin
        fields = ('url', 'id', 'ama_name', 'ama_type', 'ama_level', 'ama_isgroup', 'ama_isactive', 'ama_created', 'ama_creater', 'ama_updated', 'ama_updater')

