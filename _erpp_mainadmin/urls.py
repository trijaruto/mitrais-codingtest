from django.conf.urls import url
from . import views

app_name = "_erpp_mainadmin"
urlpatterns = [
    url(r'^$', views.indexAdminClass.as_view(), name="index")
]