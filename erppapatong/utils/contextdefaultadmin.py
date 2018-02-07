from django.urls import reverse
from _erpp_authadmin.models import useraccountadmin
from django.conf import settings

class ContextDefaultAdmin(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def on_get_context_notinsession_admin(self):
        self.context['url_logn_dash'] = reverse('_erpp_authadmin:login')
        self.context['url_sign_logt'] = reverse('_erpp_authadmin:signup')
        self.context['logn_dash'] = 'Login'
        self.context['sign_logt'] = 'Signup'
        return self.context

    def on_get_context_insession_admin(self):
        uaa_username_session = self.request.session['session_username_admin']
        self.context['url_logn_dash'] = reverse('_erpp_dasboardadmin:dasboard')
        self.context['url_sign_logt'] = reverse('_erpp_authadmin:onlogout')
        self.context['icon_logn_dash'] = '<i class="user icon"></i>'
        self.context['icon_sign_logt'] = '<i class="power icon"></i>'
        self.context['logn_dash'] = uaa_username_session
        self.context['sign_logt'] = 'Logout'
        #ACCES APPMASTERADMIN ADMINISTRATOR
        try:
            uaa_account = useraccountadmin.objects.get(uaa_username = uaa_username_session)
        except(KeyError, useraccountadmin.DoesNotExist):
            pass
        else:
            self.context['uaa_isactive'] = uaa_account.uaa_isactive
            if uaa_account.uaa_usertypeadmin.uta_name == settings.APP_DEFAULT_ACCOUNT_ADMINISTRATOR_TYPE[0]:
                #self.context['isadministrator'] = True
                self.context['menuadmin'] = self.get_context_html_menu_administrator()
            else:
                #self.context['isadministrator'] = False
                self.context['menuadmin'] = self.get_context_html_menu_admin()
        return self.context

    def get_context_html_menu_administrator(self):
        contextmenu = ('<a class="header item" href="'+reverse('_erpp_dasboardadmin:appmasteradmin-list')+'">'
                          '<i class="desktop icon"></i>' 
                          'App Master Admin'
                       '</a>'
                       + self.get_context_html_menu())
        return contextmenu

    def get_context_html_menu_admin(self):
        contextmenu = ('<a class="header item">' 
                           '<i class="desktop icon"></i>' 
                           'Menu Admin' 
                       '</a>'
                       + self.get_context_html_menu())
        return contextmenu

    def get_context_html_menu(self):
        contextmenu = ( self.get_context_appmasteradmin_menu_list() +
                        '<div class="right menu">' 
                           '<div class="item">' 
                               '<div class="ui action left icon input">' 
                                   '<i class="search icon"></i>' 
                                   '<input type="text" placeholder="Search menu">' 
                                   '<button class="ui button">Submit</button>' 
                               '</div>' 
                           '</div>' 
                       '</div>')
        return contextmenu

    def get_context_appmasteradmin_menu_list(self):
        contextmenu = ('<div class="ui dropdown item">'
                           '<i class="folder outline icon"></i>'
                           'level 1'                           
                           '<div class="menu">'
                                +self.get_context_appmasteradmin_submenu_list()+
                           '</div>'
                       '</div>')
        return contextmenu

    def get_context_appmasteradmin_submenu_list(self):
        contextmenu = ('<div class="ui dropdown item">'                      
                           '<i class="folder outline icon"></i>'
                           'level 2'
                           '<div class="menu">'
                               '<a href="#" class="item">'
                                    '<i class="file text outline icon"></i>'
                                    'ini submenu form dopdown'
                                '</a>'
                           '</div>'
                       '</div>')
        return contextmenu