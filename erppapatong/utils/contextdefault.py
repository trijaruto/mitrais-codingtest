from django.urls import reverse

class ContextDefault(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def on_get_context_notinsession(self):
        #self.context['url_logn_dash'] = reverse('erpp_auth:login')
        #self.context['url_sign_logt'] = reverse('erpp_auth:signup')
        self.context['logn_dash'] = 'Login'
        self.context['sign_logt'] = 'Signup'
        return self.context

    def on_get_context_insession(self):
        #self.context['url_logn_dash'] = reverse('erpp_dasboard:dasboard')
        #self.context['url_sign_logt'] = reverse('erpp_auth:onlogout')
        self.context['icon_logn_dash'] = '<i class="user icon"></i>'
        self.context['icon_sign_logt'] = '<i class="power icon"></i>'
        self.context['logn_dash'] = self.request.session['session_username']
        self.context['sign_logt'] = 'Logout'
        return self.context

