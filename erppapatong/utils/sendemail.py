import base64

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.urls import reverse
from erppapatong.utils.aescrypto import AESCrypto
from datetime import datetime

class SendEmail(object):
    path_email = 'erppapatong/email/'
    from_email = settings.APP_EMAIL
    bcc_email = settings.BCC_EMAIL
    context = {
        'appname' : settings.APP_NAME,
        'corpname' : settings.CORP_NAME,
        'corpaddress' : settings.CORP_ADDRESS,
        'urldomainapp' : settings.DOMAIN_NAME
    }

    def __init__(self):
        pass

    def send_email_activation(self, useraccount):
        subject = settings.APP_NAME+' Activation account, '+useraccount.ua_username
        to_email = [useraccount.ua_username,]
        template_file = self.path_email+'signupactivation.html'

        #AESCRYPTO
        url_encrypt = AESCrypto(settings.AES_KEY)
        url_encryptAES = url_encrypt.on_encrypt(str(useraccount.ua_username)+':'+str(datetime.now()))
        self.context['ua_username'] =  useraccount.ua_username
        self.context['urlactivating'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('erpp_auth:activation', kwargs={'purluaactivationcode': url_encryptAES})
        self.context['urllogin'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('erpp_auth:login')
        self.context['urlremoveaccount'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('erpp_auth:removeaccount', kwargs={'purluaactivationcode': url_encryptAES})

        html_content = render_to_string(template_file, self.context)
        text_content = strip_tags(html_content)
        self.send_email(html_content, subject, text_content, self.from_email, to_email, self.bcc_email)

    def send_email_reset_password(self, useraccount):
        subject = settings.APP_NAME+' Password Reset'
        to_email = [useraccount.ua_username,]
        template_file = self.path_email+'resetpassword.html'

        #AESCRYPTO
        url_encrypt = AESCrypto(settings.AES_KEY)
        url_encryptAES = url_encrypt.on_encrypt(str(useraccount.ua_username)+':'+str(datetime.now()))
        self.context['ua_username'] =  useraccount.ua_username
        self.context['urlresetpassword'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('erpp_auth:resetpassword', kwargs={'purlresetpassword': url_encryptAES})
        self.context['urllogin'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('erpp_auth:login')

        html_content = render_to_string(template_file, self.context)
        text_content = strip_tags(html_content)
        self.send_email(html_content, subject, text_content, self.from_email, to_email, self.bcc_email)

    def send_email_reset_password_administrator(self, useraccountadmin, uaa_userpassword_token):
        subject = settings.APP_NAME+' Your Account Administrator, '+useraccountadmin.uaa_username+', has been reset'
        to_email = [useraccountadmin.uaa_username,]
        template_file = self.path_email+'resetpasswordadministrator.html'

        self.context['uaa_username'] =  useraccountadmin.uaa_username
        self.context['uaa_userpassword'] = uaa_userpassword_token
        self.context['urllogin'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('_erpp_authadmin:login')

        html_content = render_to_string(template_file, self.context)
        text_content = strip_tags(html_content)
        self.send_email(html_content, subject, text_content, self.from_email, to_email, self.bcc_email)

    def send_email_request_activation_to_administrator(self, useraccountadmin):
        subject = settings.APP_NAME+' Request Activation Code, '+useraccountadmin.uaa_username
        to_email = [settings.APP_DEFAULT_ACCOUNT_ADMINISTRATOR_USERNAME,]
        template_file = self.path_email+'signuprequestactivationadmin.html'

        #AESCRYPTO
        url_encrypt = AESCrypto(settings.AES_KEY)
        url_encryptAES = url_encrypt.on_encrypt(str(useraccountadmin.uaa_username)+':'+str(datetime.now()))
        self.context['uaa_username'] =  useraccountadmin.uaa_username
        self.context['urlsendactivationcode'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('_erpp_authadmin:sendactivation', kwargs={'purlsenduaactivationcode': url_encryptAES})
        self.context['urlremoveaccount'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('_erpp_authadmin:removeaccount', kwargs={'purluaaremovecode': url_encryptAES})
        self.context['urllogin'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('_erpp_authadmin:login')

        html_content = render_to_string(template_file, self.context)
        text_content = strip_tags(html_content)
        self.send_email(html_content, subject, text_content, self.from_email, to_email, self.bcc_email)

    def send_email_link_activation_admin(self, useraccountadmin):
        subject = settings.APP_NAME+' Activation Account Admin, '+useraccountadmin.uaa_username
        to_email = [useraccountadmin.uaa_username,]
        template_file = self.path_email+'signupactivationadmin.html'

        #AESCRYPTO
        url_encrypt = AESCrypto(settings.AES_KEY)
        url_encryptAES = url_encrypt.on_encrypt(str(useraccountadmin.uaa_username)+':'+str(datetime.now()))
        self.context['uaa_username'] =  useraccountadmin.uaa_username
        self.context['urlactivating'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('_erpp_authadmin:activation', kwargs={'purluaactivationcode': url_encryptAES})
        self.context['urlremoveaccount'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('_erpp_authadmin:removeaccount', kwargs={'purluaaremovecode': url_encryptAES})
        self.context['urllogin'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('_erpp_authadmin:login')

        html_content = render_to_string(template_file, self.context)
        text_content = strip_tags(html_content)
        self.send_email(html_content, subject, text_content, self.from_email, to_email, self.bcc_email)

    def send_email_reset_password_admin(self, useraccountadmin):
        subject = settings.APP_NAME+' Password Reset Admin'
        to_email = [useraccountadmin.uaa_username,]
        template_file = self.path_email+'resetpasswordadmin.html'

        #AESCRYPTO
        url_encrypt = AESCrypto(settings.AES_KEY)
        url_encryptAES = url_encrypt.on_encrypt(str(useraccountadmin.uaa_username)+':'+str(datetime.now()))
        self.context['uaa_username'] =  useraccountadmin.uaa_username
        self.context['urlresetpassword'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('_erpp_authadmin:resetpassword', kwargs={'purlresetpassword': url_encryptAES})
        self.context['urllogin'] = settings.SERVER_SCHEMES+settings.DOMAIN_NAME+reverse('_erpp_authadmin:login')

        html_content = render_to_string(template_file, self.context)
        text_content = strip_tags(html_content)
        self.send_email(html_content, subject, text_content, self.from_email, to_email, self.bcc_email)


    def send_email(self, html_content, subject, text_content, from_email, to_email, bcc_email):
        if settings.BCC_EMAIL_ACTIVE:
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email, bcc_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        else:
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

