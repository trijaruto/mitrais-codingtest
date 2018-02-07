from django.conf.urls import url
from . import views

app_name = 'erpp_dasboard'
urlpatterns = [
	url(r'^dasboard/$', views.dasboardClass.as_view(), name="dasboard"),
	url(r'^dasboard/sendactivation/$', views.onSendEmailActivation.as_view(), name="sendactivation"),
]