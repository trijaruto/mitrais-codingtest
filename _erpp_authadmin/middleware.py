from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from datetime import datetime, timedelta
from django.conf import settings
from django.shortcuts import render
from erppapatong.utils.checkconnection import CheckConnectionTo

class ErpAuthAdminSessionExpiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if CheckConnectionTo().on_check_connection_to() :
            if 'session_id_admin' not in request.session:
                return self.get_response(request)
            else:
                try:
                    if datetime.now() - request.session['session_last_admin'] > timedelta( 0, settings.SESSION_AUTO_LOGOUT * 60, 0):
                        request.session.flush()
                        messages.info(request, 'Session has been expired!')
                        return HttpResponseRedirect(reverse('_erpp_authadmin:login', ))
                except KeyError:
                    pass
                request.session['session_last_admin'] = datetime.now()
            return self.get_response(request)
        else:
            context = {
                'title' : 'No Internet Connection',
                'noteerror' : 'OOPS! - No Internet Connection for this Server',
                'emailadministrator' : settings.APP_DEFAULT_ACCOUNT_ADMINISTRATOR_USERNAME,
            }
            template_name = 'erpp_main/nocon.html'
            return render(request, template_name, context)