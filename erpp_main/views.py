from django.shortcuts import render
from django.views import generic
from erppapatong.utils.contextdefault import ContextDefault

# Create your views here.
class indexClass(generic.View):
    template_name = 'erpp_main/index.html'
    def get(self, request, *args, **kwargs):
        context = {
            'title' : 'ERP Papatong',
        }

        if 'session_id' in request.session:
            context = ContextDefault(context, request).on_get_context_insession()
        else:
            context = ContextDefault(context, request).on_get_context_notinsession()

        return render(request, self.template_name, context)