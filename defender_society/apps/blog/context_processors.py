# -*- coding: utf-8 -*-


from django.conf import settings
from .utils import site_full_url


# Custom context manager
def settings_info(request):
    return {
        'site_logo_name': settings.SITE_LOGO_NAME,
        'site_end_title': settings.SITE_END_TITLE,
        'site_description': settings.SITE_DESCRIPTION,
        'site_keywords': settings.SITE_KEYWORDS,
        'api_flag': settings.API_FLAG,
        'cnzz_protocol': settings.CNZZ_PROTOCOL,
        'site_verification': settings.MY_SITE_VERIFICATION,
        'site_url': site_full_url(),
    }
