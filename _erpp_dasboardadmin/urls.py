from django.conf.urls import url
from . import views

app_name = '_erpp_dasboardadmin'
urlpatterns = [
	url(r'^dasboard/$', views.DasboardClass.as_view(), name="dasboard"),
	url(r'^dasboard/requestactivation/$', views.OnRequestActivation.as_view(), name="requestactivation"),

	#APPMASTERADMIN
	url(r'^dasboard/appmasteradmin/list/$', views.AppMasterAdminListClass.as_view(), name="appmasteradmin-list"),
	url(r'^dasboard/appmasteradmin/form/(?P<purlevent>\w+)/(?P<pk>[0-9]+)/$', views.AppMasterAdminFormClass.as_view(), name="appmasteradmin-form"),
]