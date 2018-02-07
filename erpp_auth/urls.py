from django.conf.urls import url
from . import views

app_name = 'erpp_auth'
urlpatterns = [
	url(r'^login/$', views.LoginClass.as_view(), name="login"),
	url(r'^signup/$', views.SignupClass.as_view(), name="signup"),
	url(r'^onlogin/$', views.OnLoginClass.as_view(), name="onlogin"),
	url(r'^onsignup/$', views.OnSignupClass.as_view(), name="onsignup"),
	url(r'^onlogout/$', views.OnLogoutClass.as_view(), name="onlogout"),
	url(r'^activation/(?P<purluaactivationcode>\w.+)/$', views.ActivationClass.as_view(), name="activation"),
	url(r'^removeaccount/(?P<purluaactivationcode>\w.+)/$', views.RemoveAccountClass.as_view(), name="removeaccount"),
	url(r'^forgotpassword/$', views.ForgotPasswordClass.as_view(), name="forgotpassword"),
	url(r'^onforgotpassword/$', views.OnForgotPasswordClass.as_view(), name="onforgotpassword"),
	url(r'^resetpassword/(?P<purlresetpassword>\w.+)/$', views.ResetPasswordClass.as_view(), name="resetpassword"),
	url(r'^onresetpassword/$', views.OnResetPasswordClass.as_view(), name="onresetpassword"),
]