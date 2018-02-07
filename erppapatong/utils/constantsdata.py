from django.conf import settings

class ConstantsData(object):
    #SERVER SCHEMES
    SERVER_SCHEMES = settings.SERVER_SCHEMES+settings.DOMAIN_NAME

    #PAGE
    PAGE_LIST = "list"
    PAGE_FORM = "form"
    PAGE_DETAIL = "detail"

    #FORM EVENT
    EVENT_VIEW = "view"
    EVENT_NEW = "new"
    EVENT_EDIT = "edit"
    EVENT_DELETE = "delete"

