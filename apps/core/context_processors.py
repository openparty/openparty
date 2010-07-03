from django.conf import settings # import the settings file

def analytics_id(context):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'ANALYTICS_ID': settings.ANALYTICS_ID}
