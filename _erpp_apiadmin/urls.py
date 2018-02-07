from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

#schema_view = get_schema_view(title='Pastebin API')

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api-auth/', include('rest_framework.urls')),

    # ROOT API
    url(r'^$', views.api_root),

    # INDEX ROOT API (USERS)
    url(r'^user/$', views.api_user_index, name='user-index'),
    url(r'^user/list/$', views.UserList.as_view(), name='user-list'),
    url(r'^user/list/detail/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),

    # INDEX ROOT API (USERTYPEADMIN)
    url(r'^usertypeadmin/$', views.api_usertypeadmin_index, name='usertypeadmin-index'),
    url(r'^usertypeadmin/list/$', views.UserTypeAdminList.as_view(), name='usertypeadmin-list'),
    url(r'^usertypeadmin/list/detail/(?P<pk>[0-9]+)/$', views.UserTypeAdminDetail.as_view(), name='usertypeadmin-detail'),

    # INDEX ROOT API (USERACCOUNTADMIN)
    url(r'^useraccountadmin/$', views.api_useraccountadmin_index, name='useraccountadmin-index'),
    url(r'^useraccountadmin/list/$', views.UserAccountAdminList.as_view(), name='useraccountadmin-list'),
    url(r'^useraccountadmin/list/detail/(?P<pk>[0-9]+)/$', views.UserAccountAdminDetail.as_view(), name='useraccountadmin-detail'),

    # INDEX ROOT API (APPMASTERADMIN)
    url(r'^appmasteradmin/$', views.api_appmasteradmin_index, name='appmasteradmin-index'),
    url(r'^appmasteradmin/list/$', views.AppMasterAdminList.as_view(), name='appmasteradmin-list'),
    url(r'^appmasteradmin/list/detail/(?P<pk>[0-9]+)/$', views.AppMasterAdminDetail.as_view(), name='appmasteradmin-detail'),

    url(r'^appmasteradmin/not/root/type/list/$', views.api_appmasteradmin_not_root_type_list.as_view(), name='appmasteradmin-type-not-root-list'),

    # * CUSTOME API FOR FANCY TREE (APPMASTERADMIN)
    url(r'^appmasteradmin/fancytree/list/type/(?P<ama_type>\w+)/$', views.AppMasterAdmin_Type_ForFancyTreeList.as_view(), name='appmasteradmin-type-for-fancytree-list'),
    url(r'^appmasteradmin/fancytree/list/type/(?P<ama_type>\w+)/level/(?P<ama_level>\w+)/$', views.AppMasterAdmin_Type_Level_ForFancyTreeList.as_view(), name='appmasteradmin-type-level-for-fancytree-list'),

    url(r'^appmasteradmin/inner/appmasteradminstructure/by/parentid/(?P<amas_appmasteradmin_parent_id>\w+)/fancytree/list/$', views.AppMasterAdmin_Inner_AppMasterAdminStructure_By_ParentId_ForFancyTreeList.as_view(), name='appmasteradmin-inner-appmasteradminstructure-by-parentid-forfancytreelist'),


])
