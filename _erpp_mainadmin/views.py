from django.shortcuts import render
from django.views import generic
from erppapatong.utils.contextdefaultadmin import ContextDefaultAdmin

# Create your views here.
class indexAdminClass(generic.View):
    template_name = '_erpp_mainadmin/indexadmin.html'
    def get(self, request, *args, **kwargs):
        context = {
            'title' : 'ERP Papatong Admin',
        }

        if 'session_id_admin' in request.session:
            context = ContextDefaultAdmin(context, request).on_get_context_insession_admin()
        else:
            context = ContextDefaultAdmin(context, request).on_get_context_notinsession_admin()

        return render(request, self.template_name, context)