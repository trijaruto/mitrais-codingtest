import urllib
import urllib.request
#import urllib2
import json
from django.conf import settings

class Recaptcha(object):
    url = settings.RECAPTCHA_SITEVERIFY_URL
    def __init__(self):
        pass

    def recaptcha_google(self, r_response):
        values = {
            'secret': settings.RECAPTCHA_SECRETKEY,
            'response': r_response
        }
        url_data = urllib.parse.urlencode(values)
        url_data = url_data.encode('utf-8')
        d_request = urllib.request.Request(self.url, url_data)
        d_response = urllib.request.urlopen(d_request)
        return json.load(d_response)

