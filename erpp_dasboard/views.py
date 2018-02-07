from django.shortcuts import render

from datetime import datetime
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import transaction
from django.conf import settings
from erpp_auth.models import useraccount
from erppapatong.utils.aescrypto import AESCrypto
from erppapatong.utils.contextdefault import ContextDefault
from erppapatong.utils.sendemail import SendEmail
from erppapatong.utils.checkconnection import CheckConnectionTo
from django.contrib import messages
import base64

# Create your views here.
class dasboardClass(generic.View):
    template_name = 'erpp_dasboard/dasboard.html'
    def get(self, request, *args, **kwargs):
        context = {
            'title' : 'Dasboard',
        }

        if 'session_id' not in request.session:
            return HttpResponseRedirect(reverse('erpp_main:index', ))
        else:
            context = ContextDefault(context, request).on_get_context_insession()
            try:
                u_account = useraccount.objects.get(ua_username = request.session['session_username'])
            except(KeyError, useraccount.DoesNotExist):
                pass
            else:
                context['ua_isactive'] = u_account.ua_isactive

        return render(request, self.template_name, context)

class onSendEmailActivation(generic.View):
    template_name = 'erpp_dasboard/signupactivation.html'
    def get(self, request, *args, **kwargs):
        ua_username_session = request.session['session_username']
        try:
            u_account = useraccount.objects.get(ua_username = ua_username_session)
        except(KeyError, useraccount.DoesNotExist):
            pass
        else:
            with transaction.atomic():
                #SEND EMAIL ACTIVATION
                if CheckConnectionTo().on_check_connection_to() :
                    sendemail = SendEmail();
                    sendemail.send_email_activation(u_account);
                    messages.info(request, 'your email activation has been send to '+request.session['session_username'])
                else:
                    messages.info(request, 'cannot send email activation, contact your administrator!')

        return HttpResponseRedirect(reverse('erpp_dasboard:dasboard', ), messages)
