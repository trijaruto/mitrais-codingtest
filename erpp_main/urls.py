from django.conf.urls import url
from . import views

app_name = 'erpp_main'
urlpatterns = [
	url(r'^$', views.indexClass.as_view(), name="index")
]