from django.conf import settings # import the settings file

def global_settings_injection(context):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {
        'ANALYTICS_ID': settings.ANALYTICS_ID,
        'COMMENT_SYSTEM': settings.COMMENT_SYSTEM,
        'SITE_URL': settings.SITE_URL,
    }

