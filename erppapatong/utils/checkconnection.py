from django.conf import settings
try:
    import httplib
except:
    import http.client as httplib

class CheckConnectionTo(object):
    def __init__(self):
        self.checkconnectto = settings.SERVER_CHECK_CONNECTION_TO

    def on_check_connection_to(self):
        conn = httplib.HTTPConnection(self.checkconnectto, timeout=5)
        try:
            conn.request("HEAD", "/")
            conn.close()
            return True
        except:
            conn.close()
            return False