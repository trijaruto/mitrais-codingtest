from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from _erpp_authadmin.models import useraccountadmin
from erppapatong.utils.sendemail import SendEmail
from erppapatong.utils.contextdefaultadmin import ContextDefaultAdmin
from erppapatong.utils.constantsdata import ConstantsData


# Create your views here.
class DasboardClass(generic.View):
    template_name = '_erpp_dasboardadmin/dasboardadmin.html'
    def get(self, request, *args, **kwargs):
        context = {
            'title' : 'Dasboard',
        }

        if 'session_id_admin' not in request.session:
            return HttpResponseRedirect(reverse('_erpp_mainadmin:index', ))
        else:
            context = ContextDefaultAdmin(context, request).on_get_context_insession_admin()

        return render(request, self.template_name, context)

class OnRequestActivation(generic.View):
    def get(self, request, *args, **kwargs):
        uaa_username_session = request.session['session_username_admin']
        try:
            uaa_account = useraccountadmin.objects.get(uaa_username = uaa_username_session)
        except(KeyError, useraccountadmin.DoesNotExist):
            pass
        else:
            #SEND EMAIL REQUEST ACTIVATION
            sendemail = SendEmail();
            sendemail.send_email_request_activation_to_administrator(uaa_account);
            messages.info(request, 'your request email activation has been send to administrator')

        return HttpResponseRedirect(reverse('_erpp_dasboardadmin:dasboard', ), messages)


class AppMasterAdminListClass(generic.View):
    template_name = '_erpp_dasboardadmin/appmasteradminlist.html'
    def get(self, request,  *args, **kwargs):
        context = {
            'title' : 'Dasboard',
        }

        if 'session_id_admin' not in request.session:
            return HttpResponseRedirect(reverse('_erpp_mainadmin:index', ))
        else:
            context = ContextDefaultAdmin(context, request).on_get_context_insession_admin()
            context['formlist'] = True
            context['constantsdata'] = ConstantsData

        return render(request, self.template_name, context)

class AppMasterAdminFormClass(generic.View):
    template_name = '_erpp_dasboardadmin/appmasteradminform.html'
    def get(self, request, purlevent, pk, *args, **kwargs):
        context = {
            'title' : 'Dasboard',
        }

        print("OnNewAppMasterAdminClass event : "+purlevent)
        print("OnNewAppMasterAdminClass pk : "+pk)

        if 'session_id_admin' not in request.session:
            return HttpResponseRedirect(reverse('_erpp_mainadmin:index', ))
        else:
            context = ContextDefaultAdmin(context, request).on_get_context_insession_admin()
            context['constantsdata'] = ConstantsData

        if purlevent == ConstantsData.EVENT_VIEW :
            context['appformevent'] = ConstantsData.EVENT_VIEW
        elif purlevent == ConstantsData.EVENT_NEW :
            context['appformevent'] = ConstantsData.EVENT_NEW
            print("AppMasterAdminFormClass : "+purlevent)
        elif purlevent == ConstantsData.EVENT_EDIT :
            context['appformevent'] = ConstantsData.EVENT_EDIT
        elif purlevent == ConstantsData.EVENT_DELETE :
            context['appformevent'] = ConstantsData.EVENT_DELETE
        else:
            #CHANGE TO ERROR 404
            return HttpResponseRedirect(reverse('_erpp_mainadmin:index', ))

        return render(request, self.template_name, context)

