from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from _erpp_authadmin.models import useraccountadmin, usertypeadmin
from _erpp_dasboardadmin.models import appmasteradmin
from .serializers import UserSerializer, UserAccountAdminSerializer, UserTypeAdminSerializer, AppMasterAdminSerializer

# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'user-index': reverse('user-index', request=request, format=format),
        'usertypeadmin-index': reverse('usertypeadmin-index', request=request, format=format),
        'useraccountadmin-index': reverse('useraccountadmin-index', request=request, format=format),
        'appmasteradmin-index': reverse('appmasteradmin-index', request=request, format=format),
    })

# USER REST
@api_view(['GET'])
def api_user_index(request, format=None):
    return Response({
        'user-list': reverse('user-list', request=request, format=format),
    })

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )


# USERTYPEADMIN
@api_view(['GET'])
def api_usertypeadmin_index(request, format=None):
    return Response({
        'usertypeadmin-list': reverse('usertypeadmin-list', request=request, format=format),
    })

class UserTypeAdminList(generics.ListCreateAPIView):
    queryset = usertypeadmin.objects.all()
    serializer_class = UserTypeAdminSerializer
    permission_classes = (permissions.IsAuthenticated, )

class UserTypeAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = usertypeadmin.objects.all()
    serializer_class = UserTypeAdminSerializer
    permission_classes = (permissions.IsAuthenticated, )


# USERACCOUNTADMIN
@api_view(['GET'])
def api_useraccountadmin_index(request, format=None):
    return Response({
        'useraccountadmin-list': reverse('useraccountadmin-list', request=request, format=format),
    })

class UserAccountAdminList(generics.ListAPIView):
    queryset = useraccountadmin.objects.all()
    serializer_class = UserAccountAdminSerializer
    permission_classes = (permissions.IsAuthenticated, )

class UserAccountAdminDetail(generics.RetrieveAPIView):
    queryset = useraccountadmin.objects.all()
    serializer_class = UserAccountAdminSerializer
    permission_classes = (permissions.IsAuthenticated, )


# APPMASTERINDEX
@api_view(['GET'])
def api_appmasteradmin_index(request, format=None):
    return Response({
        'appmasteradmin-list': reverse('appmasteradmin-list', request=request, format=format),
        'appmasteradmin-type-not-root-list': reverse('appmasteradmin-type-not-root-list', request=request, format=format),
        'appmasteradmin-type-for-fancytree-list': reverse('appmasteradmin-type-for-fancytree-list', request=request, format=format, kwargs={'ama_type': 'ROT'}),
        'appmasteradmin-type-level-for-fancytree-list': reverse('appmasteradmin-type-level-for-fancytree-list', request=request, format=format, kwargs={'ama_type': 'ROT', 'ama_level':'0'}),
        'appmasteradmin-inner-appmasteradminstructure-by-parentid-forfancytreelist' : reverse('appmasteradmin-inner-appmasteradminstructure-by-parentid-forfancytreelist', request=request, format=format, kwargs={'amas_appmasteradmin_parent_id': '1'}),
    })

class AppMasterAdminList(generics.ListCreateAPIView):
    queryset = appmasteradmin.objects.all()
    serializer_class = AppMasterAdminSerializer
    permission_classes = (permissions.IsAuthenticated, )

class AppMasterAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = appmasteradmin.objects.all()
    serializer_class = AppMasterAdminSerializer
    permission_classes = (permissions.IsAuthenticated, )

class api_appmasteradmin_not_root_type_list(APIView):
    def get(self, request):
        ama_type_list = appmasteradmin.TYPE
        ama_type_arr = []
        for key, name in ama_type_list:
            if key!="ROT":
                records = {
                    'key' :key,
                    'name' : name,
                }
                ama_type_arr.append(records)
        return Response(ama_type_arr)

class AppMasterAdmin_Type_ForFancyTreeList(APIView):
    def get(self, request, ama_type):
        ama_list = appmasteradmin.objects.filter(ama_type=ama_type)
        ama_arr = []
        for ama in ama_list:
            records = {
                'key' : ama.id,
                'title' : ama.ama_name,
                'folder' : ama.ama_isgroup,
                'lazy' : True,
                'type' : ama.ama_level
            }
            ama_arr.append(records)
        return Response(ama_arr)

class AppMasterAdmin_Type_Level_ForFancyTreeList(APIView):
    def get(self, request, ama_type, ama_level):
        ama_list = appmasteradmin.objects.filter(ama_type=ama_type, ama_level=ama_level)
        ama_arr = []
        for ama in ama_list:
            records = {
                'key' : ama.id,
                'title' : ama.ama_name,
                'folder' : ama.ama_isgroup,
                'lazy' : True,
                'type' : ama.ama_level
            }
            ama_arr.append(records)
        return Response(ama_arr)

class AppMasterAdmin_Inner_AppMasterAdminStructure_By_ParentId_ForFancyTreeList(APIView):
    def get(self, request, amas_appmasteradmin_parent_id):
        ama_list = appmasteradmin.objects.raw("SELECT _erpp_da_ama.id, _erpp_da_ama.ama_name, _erpp_da_ama.ama_isgroup  FROM _erpp_dasboardadmin_appmasteradmin AS _erpp_da_ama " \
                                              "INNER JOIN _erpp_dasboardadmin_appmasteradminstructure _erpp_da_amas " \
                                              "ON _erpp_da_amas.amas_appmasteradmin_child_id = _erpp_da_ama.id " \
                                              "WHERE " \
                                              "_erpp_da_amas.amas_appmasteradmin_parent_id = %s " \
                                              "AND " \
                                              "_erpp_da_ama.ama_type NOT IN ('ROT') ",  [amas_appmasteradmin_parent_id] )
        ama_arr = []
        for ama in ama_list:
            records = {
                'key' : ama.id,
                'title' : ama.ama_name,
                'folder' : ama.ama_isgroup,
                'lazy' : True,
                'type' : ama.ama_level
            }
            ama_arr.append(records)
        return Response(ama_arr)



@api_view(['GET'])
def api_root_custom(request, format=None):
    return Response({
        'custom-json': reverse('custom-json', request=request, format=format),
    })

class CustomJSon(APIView):
    def get(self, request):
        return Response({'some': 'data'})


