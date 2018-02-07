import bcrypt
from datetime import datetime, timedelta
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import transaction
from django.conf import settings
from django.contrib import messages
from erppapatong.utils.aescrypto import AESCrypto
from erppapatong.utils.sendemail import SendEmail
from erppapatong.utils.recaptcha import Recaptcha
from erppapatong.utils.contextdefault import ContextDefault
from erppapatong.utils.checkconnection import CheckConnectionTo
from .models import useraccount

# Create your views here.sdf
class LoginClass(generic.View):
    template_name = 'erpp_auth/login.html'
    def get(self, request, *args, **kwargs):
        context = {
            'title' : 'Login',
        }

        if 'session_id' in request.session:
            return HttpResponseRedirect(reverse('erpp_dasboard:dasboard', ))
        else:
            context = ContextDefault(context, request).on_get_context_notinsession()

        return render(request, self.template_name, context)

class OnLoginClass(generic.View):
    def post(self, request, *args, **kwargs):
        ua_username_name = request.POST.get('ua_username_name', None)
        ua_userpassword_name = request.POST.get('ua_userpassword_name', None)
        try:
            ua_exist = useraccount.objects.get(ua_username = ua_username_name)
        except(KeyError, useraccount.DoesNotExist):
            messages.info(request, 'Wrong username or password!')
            return HttpResponseRedirect(reverse('erpp_auth:login', ))
        else:
            if bcrypt.checkpw(str(ua_userpassword_name).encode("utf-8"), str(ua_exist.ua_userpassword).encode("utf-8")):
                #request.session.flush()
                request.session['session_id'] = ua_exist.id
                request.session['session_username'] = ua_exist.ua_username
                return HttpResponseRedirect(reverse('erpp_dasboard:dasboard', ))
            else:
                messages.info(request, 'Wrong username or password!')
                return HttpResponseRedirect(reverse('erpp_auth:login', ))
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('erpp_auth:login', ))

class SignupClass(generic.View):
    template_name = 'erpp_auth/signup.html'
    def get(self, request, *args, **kwargs):
        context = {
            'title' : 'Signup',
            'sitekey_recaptcha' : settings.RECAPTCHA_SITEKEY,
        }

        if 'session_id' in request.session:
            return HttpResponseRedirect(reverse('erpp_dasboard:dasboard', ))
        else:
            context = ContextDefault(context, request).on_get_context_notinsession()

        return render(request, self.template_name, context)

class OnSignupClass(generic.View):
    def post(self, request, *args, **kwargs):
        ua_username_name = request.POST.get('ua_username_name', None)
        ua_userpassword_name = request.POST.get('ua_userpassword_name', None)

        #RECAPTCHA
        req_recaptcha = request.POST.get('g-recaptcha-response')
        res_recaptcha = Recaptcha().recaptcha_google(req_recaptcha)

        try:
            ua_exist = useraccount.objects.get(ua_username = ua_username_name)
        except(KeyError, useraccount.DoesNotExist):
            if res_recaptcha['success']:
                if request.method == 'POST':
                    ua = useraccount(ua_username = ua_username_name,
                                     ua_userpassword = bcrypt.hashpw(str(ua_userpassword_name).encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                                     ua_isactive = False,
                                     ua_keystone_id = 0,
                                     ua_keystone_user_id = 'get API openstack keystone user id',
                                     ua_created = datetime.now(),
                                     ua_creater = ua_username_name,
                                     ua_updated = datetime.now(),
                                     ua_updater = ua_username_name,
                                     ua_issuspend = False,)
                with transaction.atomic():
                    ua.save()
                    #CHECK CONNECTION
                    if CheckConnectionTo().on_check_connection_to() :
                        #SEND EMAIL ACTIVATION
                        sendemail = SendEmail();
                        sendemail.send_email_activation(ua);
                    #SESSION
                    request.session['session_id'] = ua.id
                    request.session['session_username'] = ua.ua_username
                    return HttpResponseRedirect(reverse('erpp_dasboard:dasboard', ))
            else:
                messages.info(request, 'Please click reCaptcha!')
                return HttpResponseRedirect(reverse('erpp_auth:signup', ))
        else:
            messages.info(request, ua_username_name+' already exist')
            return HttpResponseRedirect(reverse('erpp_auth:signup', ))
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('erpp_auth:signup', ))

class OnLogoutClass(generic.View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return HttpResponseRedirect(reverse('erpp_auth:login', ))

class ActivationClass(generic.View):
    template_name = 'erpp_auth/activation.html'
    def get(self, request, purluaactivationcode, *args, **kwargs):
        context = {
            'title' : 'Activation',
        }

        url_dencrypt = AESCrypto(settings.AES_KEY)
        ua_activationcode_decrypt = url_dencrypt.on_decrypt(purluaactivationcode).split(':',1)
        ua_username_purl = ua_activationcode_decrypt[0]
        linkexpired_purl = ua_activationcode_decrypt[1]
        date_linkexpired_purl =  datetime.strptime(linkexpired_purl, "%Y-%m-%d %H:%M:%S.%f")

        if datetime.now() - date_linkexpired_purl > timedelta( 0, settings.EMAIL_ACTIVATION_EXPIRED * 60, 0):
            context['url_link_expired'] = True
            if 'session_id' not in request.session:
                context = ContextDefault(context, request).on_get_context_notinsession()
                context['on_session'] = False
                context['appname'] = settings.APP_NAME
                context['ua_username_purl'] = ua_username_purl
            else:
                context = ContextDefault(context, request).on_get_context_insession()
                context['on_session'] = True
                context['appname'] = settings.APP_NAME
                context['ua_username_purl'] = ua_username_purl
        else:
            context['url_link_expired'] = False
            try:
                u_account = useraccount.objects.get(ua_username = ua_username_purl)
                if 'session_id' not in request.session:
                    context = ContextDefault(context, request).on_get_context_notinsession()
                    context['on_session'] = False
                    context['appname'] = settings.APP_NAME
                    context['ua_username_purl'] = ua_username_purl
                else:
                    context = ContextDefault(context, request).on_get_context_insession()
                    context['on_session'] = True
                    context['appname'] = settings.APP_NAME
                    context['ua_username_purl'] = ua_username_purl
            except(KeyError, useraccount.DoesNotExist):
                pass
            else:
                if u_account.ua_isactive:
                    context['url_link_expired'] = True
                else:
                    with transaction.atomic():
                        u_account.ua_isactive = True
                        u_account.save()
                        context['ua_isactive'] = u_account.ua_isactive


        return render(request, self.template_name, context)

class RemoveAccountClass(generic.View):
    template_name = 'erpp_auth/removeaccount.html'
    def get(self, request, purluaactivationcode, *args, **kwargs):
        context = {
            'title' : 'Remove Account',
        }

        # ua_activationcode_encrypt = AESCrypto(settings.AES_KEY).on_decrypt(base64.b64decode(purluaactivationcode)).__str__().split(':',1)
        # ua_username_purl = ua_activationcode_encrypt[0]
        url_dencrypt = AESCrypto(settings.AES_KEY)
        ua_activationcode_decrypt = url_dencrypt.on_decrypt(purluaactivationcode).split(':',1)
        ua_username_purl = ua_activationcode_decrypt[0]
        linkexpired_purl = ua_activationcode_decrypt[1]
        date_linkexpired_purl =  datetime.strptime(linkexpired_purl, "%Y-%m-%d %H:%M:%S.%f")

        try:
            u_account = useraccount.objects.get(ua_username = ua_username_purl)
            if 'session_id' not in request.session:
                context = ContextDefault(context, request).on_get_context_notinsession()
                context['appname'] = settings.APP_NAME
                context['ua_username_purl'] = ua_username_purl
            else:
                context = ContextDefault(context, request).on_get_context_insession()
                context['appname'] = settings.APP_NAME
                context['ua_username_purl'] = ua_username_purl
        except(KeyError, useraccount.DoesNotExist):
            context['url_useraccount_doesnotexist'] = True
            context = ContextDefault(context, request).on_get_context_notinsession()
            context['appname'] = settings.APP_NAME
            context['ua_username_purl'] = ua_username_purl
        else:
            context['url_useraccount_doesnotexist'] = False
            if u_account.ua_isactive:
                context['ua_isactive'] = True
            else:
                with transaction.atomic():
                    request.session.flush()
                    context = ContextDefault(context, request).on_get_context_notinsession()
                    context['appname'] = settings.APP_NAME
                    context['ua_username_purl'] = ua_username_purl
                    u_account.delete()
                    context['ua_isactive'] = False

        return render(request, self.template_name, context)

class ForgotPasswordClass(generic.View):
    template_name = 'erpp_auth/forgotpassword.html'
    def get(self, request, *args, **kwargs):
        context = {
            'title' : 'Forgot Password',
        }

        if 'session_id' in request.session:
            return HttpResponseRedirect(reverse('erpp_dasboard:dasboard', ))
        else:
            context = ContextDefault(context, request).on_get_context_notinsession()

        return render(request, self.template_name, context)

class OnForgotPasswordClass(generic.View):
    def post(self, request, *args, **kwargs):
        ua_username_name = request.POST.get('ua_username_name', None)
        try:
            ua_exist = useraccount.objects.get(ua_username = ua_username_name)
        except(KeyError, useraccount.DoesNotExist):
            messages.info(request, 'Your email does not exist!')
            return HttpResponseRedirect(reverse('erpp_auth:forgotpassword', ))
        else:
            #SEND EMAIL FORFGOT PASSWORD
            sendemail = SendEmail();
            sendemail.send_email_reset_password(ua_exist);
            messages.info(request, 'Email for reset password has been send to '+ua_username_name)
            return HttpResponseRedirect(reverse('erpp_auth:forgotpassword', ))

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('erpp_auth:forgotpassword', ))

class ResetPasswordClass(generic.View):
    template_name = 'erpp_auth/resetpassword.html'
    def get(self, request, purlresetpassword, *args, **kwargs):
        context = {
            'title' : 'Reset Password',
            'sitekey_recaptcha' : settings.RECAPTCHA_SITEKEY,
        }

        #URL AESCRYPTO DECRYPT
        url_decrypt = AESCrypto(settings.AES_KEY)
        ua_activationcode_decrypt = url_decrypt.on_decrypt(purlresetpassword).split(':',1)
        ua_username_purl = ua_activationcode_decrypt[0]
        linkexpired_purl = ua_activationcode_decrypt[1]
        date_linkexpired_purl =  datetime.strptime(linkexpired_purl, "%Y-%m-%d %H:%M:%S.%f")

        if 'session_id' in request.session:
            return HttpResponseRedirect(reverse('erpp_dasboard:dasboard', ))
        else:
            context = ContextDefault(context, request).on_get_context_notinsession()
            if datetime.now() - date_linkexpired_purl > timedelta( 0, settings.EMAIL_RESET_PASSWORD_EXPIRED * 60, 0):
                context['url_link_expired'] = True
            else:
                context['url_link_expired'] = False
                context['url_resetpassword_value'] = purlresetpassword
                context['ua_username_value'] = ua_username_purl

        return render(request, self.template_name, context)

class OnResetPasswordClass(generic.View):
    def post(self, request, *args, **kwargs):
        purlresetpassword = request.POST.get('url_resetpassword_name', None)
        ua_username_name = request.POST.get('ua_username_name', None)
        ua_userpassword_name = request.POST.get('ua_userpassword_name', None)
        #RECAPTCHA
        req_recaptcha = request.POST.get('g-recaptcha-response')
        res_recaptcha = Recaptcha().recaptcha_google(req_recaptcha)

        try:
            u_account = useraccount.objects.get(ua_username = ua_username_name)
        except(KeyError, useraccount.DoesNotExist):
            pass
        else:
            if res_recaptcha['success']:
                with transaction.atomic():
                    u_account.ua_userpassword = bcrypt.hashpw(str(ua_userpassword_name).encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                    u_account.ua_updated = datetime.now()
                    u_account.ua_updater = ua_username_name
                    u_account.save()
                    messages.info(request, 'your password email has been reset')
            else:
                messages.info(request, 'Please click reCaptcha!')
                return HttpResponseRedirect(reverse('erpp_auth:resetpassword', kwargs={'purlresetpassword': purlresetpassword}))

        return HttpResponseRedirect(reverse('erpp_auth:login', ), messages)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('erpp_auth:login', ))
