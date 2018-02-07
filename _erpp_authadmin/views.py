from django.shortcuts import render
import bcrypt
from datetime import datetime, timedelta
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from django.conf import settings
from django.contrib import messages
from _erpp_dasboardadmin.models import appmasteradmin, appmasteradminstructure
from erppapatong.utils.aescrypto import AESCrypto
from erppapatong.utils.sendemail import SendEmail
from erppapatong.utils.recaptcha import Recaptcha
from erppapatong.utils.contextdefaultadmin import ContextDefaultAdmin
from erppapatong.utils.tokenrandom import TokenRandom
from .models import useraccountadmin, usertypeadmin

# Create your views here.
class LoginClass(generic.View):
    template_name = '_erpp_authadmin/loginadmin.html'
    def get(self, request, *args, **kwargs):
        context = {
            'title' : 'Login',
        }

        if 'session_id_admin' in request.session:
            return HttpResponseRedirect(reverse('_erpp_dasboardadmin:dasboard', ))
        else:
            context = ContextDefaultAdmin(context, request).on_get_context_notinsession_admin()

        return render(request, self.template_name, context)

class OnLoginClass(generic.View):
    def post(self, request, *args, **kwargs):
        uaa_username_name = request.POST.get('uaa_username_name', None)
        uaa_userpassword_name = request.POST.get('uaa_userpassword_name', None)
        try:
            uaa_exist = useraccountadmin.objects.get(uaa_username = uaa_username_name)
        except(KeyError, useraccountadmin.DoesNotExist):
            messages.info(request, 'Wrong username or password!')
            return HttpResponseRedirect(reverse('_erpp_authadmin:login', ))
        else:
            if bcrypt.checkpw(str(uaa_userpassword_name).encode("utf-8"), str(uaa_exist.uaa_userpassword).encode("utf-8")):
                #request.session.flush()
                request.session['session_id_admin'] = uaa_exist.id
                request.session['session_username_admin'] = uaa_exist.uaa_username
                return HttpResponseRedirect(reverse('_erpp_dasboardadmin:dasboard', ))
            else:
                messages.info(request, 'Wrong username or password!')
                return HttpResponseRedirect(reverse('_erpp_authadmin:login', ))
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('_erpp_authadmin:login', ))


class SignupClass(generic.View):
    template_name = '_erpp_authadmin/signupadmin.html'
    def get(self, request, *args, **kwargs):
        context = {
            'title' : 'Signup',
            'sitekey_recaptcha' : settings.RECAPTCHA_SITEKEY,
        }
        if 'session_id_admin' in request.session:
            return HttpResponseRedirect(reverse('_erpp_dasboardadmin:dasboard', ))
        else:
            context = ContextDefaultAdmin(context, request).on_get_context_notinsession_admin()

        return render(request, self.template_name, context)

class OnSignupClass(generic.View):
    def post(self, request, *args, **kwargs):
        uaa_username_name = request.POST.get('uaa_username_name', None)
        uaa_userpassword_name = request.POST.get('uaa_userpassword_name', None)
        #RECAPTCHA
        req_recaptcha = request.POST.get('g-recaptcha-response')
        res_recaptcha = Recaptcha().recaptcha_google(req_recaptcha)

        try:
            uaa_exist = useraccountadmin.objects.get(uaa_username = uaa_username_name)
        except(KeyError, useraccountadmin.DoesNotExist):
            if res_recaptcha['success']:
                uta_typeadmin = usertypeadmin.objects.get(uta_name = settings.APP_DEFAULT_ACCOUNT_ADMINISTRATOR_TYPE[1])
                uaa = useraccountadmin(uaa_username = uaa_username_name,
                                       uaa_userpassword = bcrypt.hashpw(str(uaa_userpassword_name).encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                                       uaa_usertypeadmin = uta_typeadmin,
                                       uaa_isactive = False,
                                       uaa_keystone_id = 0,
                                       uaa_keystone_user_id = 'get API openstack keystone user id',
                                       uaa_created = datetime.now(),
                                       uaa_creater = uaa_username_name,
                                       uaa_updated = datetime.now(),
                                       uaa_updater = uaa_username_name,
                                       uaa_issuspend = False,)
                with transaction.atomic():
                    uaa.save()
                    #SEND EMAIL ACTIVATION
                    sendemail = SendEmail();
                    sendemail.send_email_request_activation_to_administrator(uaa);
                    #SESSION
                    request.session['session_id_admin'] = uaa.id
                    request.session['session_username_admin'] = uaa.uaa_username
                    return HttpResponseRedirect(reverse('_erpp_dasboardadmin:dasboard', ))
            else:
                messages.info(request, 'Please click reCaptcha!')
                return HttpResponseRedirect(reverse('_erpp_authadmin:signup', ))
        else:
            messages.info(request, uaa_username_name+' already exist')
            return HttpResponseRedirect(reverse('_erpp_authadmin:signup', ))
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('_erpp_authadmin:signup', ))


class OnLogoutClass(generic.View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return HttpResponseRedirect(reverse('_erpp_authadmin:login', ))

class ResetPasswordAdministratorClass(generic.View):
    template_name = '_erpp_authadmin/resetpasswordadministrator.html'
    def get(self, request, *args, **kwargs):
        context = {
            'title' : 'Reset Password',
            'reset_password_admin' : settings.APP_DEFAULT_ACCOUNT_ADMINISTRATOR_RESET,
            'username_admin' : settings.APP_DEFAULT_ACCOUNT_ADMINISTRATOR_USERNAME,
        }

        if 'session_id_admin' in request.session:
            return HttpResponseRedirect(reverse('_erpp_dasboardadmin:dasboard', ))
        else:
            context = ContextDefaultAdmin(context, request).on_get_context_notinsession_admin()
        return render(request, self.template_name, context)


class OnResetPasswordAdministratorClass(generic.View):
    def post(self, request, *args, **kwargs):
        uaa_username_setting = settings.APP_DEFAULT_ACCOUNT_ADMINISTRATOR_USERNAME
        uaa_userpassword_token = ''.join(str(ptkn) for ptkn in TokenRandom.get_token_random_range(settings.APP_DEFAULT_ACCOUNT_ADMINISTRATOR_RANDOM_PASSWORD_DIGIT))
        try:
            uaa_exist = useraccountadmin.objects.get(uaa_username = uaa_username_setting)
        except(KeyError, useraccountadmin.DoesNotExist):
            with transaction.atomic():
                #CREATE USERTYPEADMIN IF DOESNOTEXIST
                uta_administrator = usertypeadmin(uta_name=settings.APP_DEFAULT_ACCOUNT_ADMINISTRATOR_TYPE[0],
                                                  uta_created = datetime.now(),
                                                  uta_creater = uaa_username_setting,
                                                  uta_updated = datetime.now(),
                                                  uta_updater = uaa_username_setting,)
                uta_administrator.save()
                uta_admin = usertypeadmin(uta_name=settings.APP_DEFAULT_ACCOUNT_ADMINISTRATOR_TYPE[1],
                                          uta_created = datetime.now(),
                                          uta_creater = uaa_username_setting,
                                          uta_updated = datetime.now(),
                                          uta_updater = uaa_username_setting,)
                uta_admin.save()
                #CREATE APPMASTERADMIN ROOT
                ama_root = appmasteradmin(id=1,
                                          ama_name = "ROOT",
                                          ama_type = appmasteradmin.TYPE[0][0],
                                          ama_level = 0,
                                          ama_isgroup = True,
                                          ama_isactive = True,
                                          ama_created = datetime.now(),
                                          ama_creater = uaa_username_setting,
                                          ama_updated = datetime.now(),
                                          ama_updater = uaa_username_setting,)
                ama_root.save()
                #CREATE APPMASTERADMINSTRUCTURE ROOT
                ama_rootstructure = appmasteradminstructure(id=1,
                                                            amas_appmasteradmin_parent = ama_root,
                                                            amas_appmasteradmin_child = ama_root,)
                ama_rootstructure.save()
                #CREATE ACCOUNT IF DOESNOTEXIST
                uaa = useraccountadmin(uaa_username = uaa_username_setting,
                                       uaa_userpassword = bcrypt.hashpw(str(uaa_userpassword_token).encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                                       uaa_isactive = True,
                                       uaa_usertypeadmin_id = uta_administrator.id,
                                       uaa_keystone_id = 0,
                                       uaa_keystone_user_id = 'get API openstack keystone user id',
                                       uaa_created = datetime.now(),
                                       uaa_creater = uaa_username_setting,
                                       uaa_updated = datetime.now(),
                                       uaa_updater = uaa_username_setting,
                                       uaa_issuspend = False,)
                uaa.save()
                #SEND EMAIL RESET PASSWORD
                sendemail = SendEmail();
                sendemail.send_email_reset_password_administrator(uaa, uaa_userpassword_token);
            messages.info(request, 'Username and password administrator has been send to your email '+uaa_username_setting)
            return HttpResponseRedirect(reverse('_erpp_authadmin:resetpasswordadministrator', ))
        else:
            with transaction.atomic():
                #UPDATE ACCOUNT IF EXIST
                uaa_exist.uaa_userpassword = bcrypt.hashpw(str(uaa_userpassword_token).encode("utf-8"), bcrypt.gensalt())
                uaa_exist.uaa_updated = datetime.now()
                uaa_exist.uaa_updater = uaa_username_setting,
                uaa_exist.save()
                #SEND EMAIL RESET PASSWORD
                sendemail = SendEmail();
                sendemail.send_email_reset_password_administrator(uaa_exist, uaa_userpassword_token);
            messages.info(request, 'Username and password administrator has been send to your email '+uaa_username_setting)
            return HttpResponseRedirect(reverse('_erpp_authadmin:resetpasswordadministrator', ))

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('_erpp_authadmin:login', ))

class SendActivationClass(generic.View):
    template_name = '_erpp_authadmin/sendactivationadmin.html'
    def get(self, request, purlsenduaactivationcode, *args, **kwargs):
        context = {
            'title' : 'Activation',
        }

        #URL AESCRYPTO DECRYPT
        url_dencrypt = AESCrypto(settings.AES_KEY)
        uaa_activationcode_decrypt = url_dencrypt.on_decrypt(purlsenduaactivationcode).split(':',1)
        uaa_username_purl = uaa_activationcode_decrypt[0]
        linkexpired_purl = uaa_activationcode_decrypt[1]
        date_linkexpired_purl =  datetime.strptime(linkexpired_purl, "%Y-%m-%d %H:%M:%S.%f")

        if datetime.now() - date_linkexpired_purl > timedelta( 0, settings.EMAIL_REQUEST_ACTIVATION_ADMIN_EXPIRED * 60, 0):
            context['url_link_expired'] = True
        else:
            context['url_link_expired'] = False

        context['uaa_username_purl_value'] = uaa_username_purl
        context['url_send_activation_code_value'] = purlsenduaactivationcode

        if 'session_id_admin' in request.session:
            context = ContextDefaultAdmin(context, request).on_get_context_insession_admin()
        else:
            context = ContextDefaultAdmin(context, request).on_get_context_notinsession_admin()

        return render(request, self.template_name, context)


class OnSendActivationClass(generic.View):
    def post(self, request, *args, **kwargs):
        uaa_username_purl_value = request.POST.get('uaa_username_purl_name', None)
        url_send_activation_code_value = request.POST.get('url_send_activation_code_name', None)
        try:
            uaa_exist = useraccountadmin.objects.get(uaa_username = uaa_username_purl_value)
        except(KeyError, useraccountadmin.DoesNotExist):
            messages.info(request, 'Useraccount '+uaa_username_purl_value+' does not exist! Contact your administrator.')
            return HttpResponseRedirect(reverse('_erpp_authadmin:sendactivation', kwargs={'purlsenduaactivationcode': url_send_activation_code_value}))
        else:
            #SEND EMAIL LINK ACTIVATION
            sendemail = SendEmail();
            sendemail.send_email_link_activation_admin(uaa_exist);

            messages.info(request, 'Link activation has been send to '+uaa_username_purl_value)
            return HttpResponseRedirect(reverse('_erpp_authadmin:sendactivation', kwargs={'purlsenduaactivationcode': url_send_activation_code_value}))

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('_erpp_authadmin:login', ))

class ActivationClass(generic.View):
    template_name = '_erpp_authadmin/activationadmin.html'
    def get(self, request, purluaactivationcode, *args, **kwargs):
        context = {
            'title' : 'Activation Admin',
        }

        #URL AESCRYPTO DECRYPT
        url_dencrypt = AESCrypto(settings.AES_KEY)
        uaa_activationcode_decrypt = url_dencrypt.on_decrypt(purluaactivationcode).split(':',1)
        uaa_username_purl = uaa_activationcode_decrypt[0]
        linkexpired_purl = uaa_activationcode_decrypt[1]
        date_linkexpired_purl =  datetime.strptime(linkexpired_purl, "%Y-%m-%d %H:%M:%S.%f")

        if datetime.now() - date_linkexpired_purl > timedelta( 0, settings.EMAIL_ACTIVATION_ADMIN_EXPIRED * 60, 0):
            context['url_link_expired'] = True
        else:
            context['url_link_expired'] = False

        context['uaa_username_purl_value'] = uaa_username_purl
        context['appname'] = settings.APP_NAME

        if 'session_id_admin' in request.session:
            context = ContextDefaultAdmin(context, request).on_get_context_insession_admin()
            context['on_session'] = True
        else:
            context = ContextDefaultAdmin(context, request).on_get_context_notinsession_admin()
            context['on_session'] = False

        try:
            uaa_exist = useraccountadmin.objects.get(uaa_username = uaa_username_purl)
        except(KeyError, useraccountadmin.DoesNotExist):
            pass
        else:
            if uaa_exist.uaa_isactive:
                context['url_link_expired'] = True
            else:
                with transaction.atomic():
                    uaa_exist.uaa_isactive = True
                    uaa_exist.save()
                    context['ua_isactive'] = uaa_exist.uaa_isactive

        return render(request, self.template_name, context)

class RemoveAccountClass(generic.View):
    template_name = '_erpp_authadmin/removeaccountadmin.html'
    def get(self, request, purluaaremovecode, *args, **kwargs):
        context = {
            'title' : 'Remove Account',
        }

        #URL AESCRYPTO DECRYPT
        url_dencrypt = AESCrypto(settings.AES_KEY)
        uaa_activationcode_decrypt = url_dencrypt.on_decrypt(purluaaremovecode).split(':',1)
        uaa_username_purl = uaa_activationcode_decrypt[0]
        linkexpired_purl = uaa_activationcode_decrypt[1]
        date_linkexpired_purl =  datetime.strptime(linkexpired_purl, "%Y-%m-%d %H:%M:%S.%f")

        try:
            uaa_account = useraccountadmin.objects.get(uaa_username = uaa_username_purl)
            if 'session_id_admin' not in request.session:
                context = ContextDefaultAdmin(context, request).on_get_context_notinsession_admin()
                context['appname'] = settings.APP_NAME
                context['uaa_username_purl'] = uaa_username_purl
            else:
                context = ContextDefaultAdmin(context, request).on_get_context_insession_admin()
                context['appname'] = settings.APP_NAME
                context['uaa_username_purl'] = uaa_username_purl
        except(KeyError, useraccountadmin.DoesNotExist):
            context['url_useraccount_doesnotexist'] = True
            context = ContextDefaultAdmin(context, request).on_get_context_notinsession_admin()
            context['appname'] = settings.APP_NAME
            context['uaa_username_purl'] = uaa_username_purl
        else:
            context['url_useraccount_doesnotexist'] = False
            if uaa_account.uaa_isactive:
                context['uaa_isactive'] = True
            else:
                with transaction.atomic():
                    request.session.flush()
                    context = ContextDefaultAdmin(context, request).on_get_context_notinsession_admin()
                    context['appname'] = settings.APP_NAME
                    context['uaa_username_purl'] = uaa_username_purl
                    uaa_account.delete()
                    context['uaa_isactive'] = False

        return render(request, self.template_name, context)

class ForgotPasswordClass(generic.View):
    template_name = '_erpp_authadmin/forgotpasswordadmin.html'
    def get(self, request, *args, **kwargs):
        context = {
            'title' : 'Forgot Password Admin',
        }

        if 'session_id' in request.session:
            return HttpResponseRedirect(reverse('_erpp_dasboardadmin:dasboard', ))
        else:
            context = ContextDefaultAdmin(context, request).on_get_context_notinsession_admin()

        return render(request, self.template_name, context)

class OnForgotPasswordClass(generic.View):
    def post(self, request, *args, **kwargs):
        uaa_username_name = request.POST.get('uaa_username_name', None)
        try:
            uaa_exist = useraccountadmin.objects.get(uaa_username = uaa_username_name)
        except(KeyError, useraccountadmin.DoesNotExist):
            messages.info(request, 'Your email does not exist!')
            return HttpResponseRedirect(reverse('_erpp_authadmin:forgotpassword', ))
        else:
            #SEND EMAIL FORFGOT PASSWORD
            sendemail = SendEmail();
            sendemail.send_email_reset_password_admin(uaa_exist);
            messages.info(request, 'Email for reset password has been send to '+uaa_username_name)
            return HttpResponseRedirect(reverse('_erpp_authadmin:forgotpassword', ))

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('_erpp_authadmin:forgotpassword', ))

class ResetPasswordClass(generic.View):
    template_name = '_erpp_authadmin/resetpasswordadmin.html'
    def get(self, request, purlresetpassword, *args, **kwargs):
        context = {
            'title' : 'Reset Password Admin',
            'sitekey_recaptcha' : settings.RECAPTCHA_SITEKEY,
        }

        #URL AESCRYPTO DECRYPT
        url_dencrypt = AESCrypto(settings.AES_KEY)
        uaa_activationcode_decrypt = url_dencrypt.on_decrypt(purlresetpassword).split(':',1)
        uaa_username_purl = uaa_activationcode_decrypt[0]
        linkexpired_purl = uaa_activationcode_decrypt[1]
        date_linkexpired_purl =  datetime.strptime(linkexpired_purl, "%Y-%m-%d %H:%M:%S.%f")

        if 'session_id' in request.session:
            return HttpResponseRedirect(reverse('_erpp_dasboardadmin:dasboard', ))
        else:
            context = ContextDefaultAdmin(context, request).on_get_context_notinsession_admin()
            if datetime.now() - date_linkexpired_purl > timedelta( 0, settings.EMAIL_RESET_PASSWORD_ADMIN_EXPIRED * 60, 0):
                context['url_link_expired'] = True
            else:
                context['url_link_expired'] = False
                context['url_resetpassword_value'] = purlresetpassword
                context['uaa_username_value'] = uaa_username_purl

        return render(request, self.template_name, context)



class OnResetPasswordClass(generic.View):
    def post(self, request, *args, **kwargs):
        purlresetpassword = request.POST.get('url_resetpassword_name', None)
        uaa_username_name = request.POST.get('uaa_username_name', None)
        uaa_userpassword_name = request.POST.get('uaa_userpassword_name', None)
        #RECAPTCHA
        req_recaptcha = request.POST.get('g-recaptcha-response')
        res_recaptcha = Recaptcha().recaptcha_google(req_recaptcha)

        try:
            uaa_account = useraccountadmin.objects.get(uaa_username = uaa_username_name)
        except(KeyError, useraccountadmin.DoesNotExist):
            pass
        else:
            if res_recaptcha['success']:
                with transaction.atomic():
                    uaa_account.uaa_userpassword = bcrypt.hashpw(str(uaa_userpassword_name).encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                    uaa_account.uaa_updated = datetime.now()
                    uaa_account.uaa_updater = uaa_username_name
                    uaa_account.save()
                    messages.info(request, 'your password admin has been reset')
            else:
                messages.info(request, 'Please click reCaptcha!')
                return HttpResponseRedirect(reverse('_erpp_authadmin:resetpassword', kwargs={'purlresetpassword': purlresetpassword}))

        return HttpResponseRedirect(reverse('_erpp_authadmin:login', ), messages)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('_erpp_authadmin:login', ))