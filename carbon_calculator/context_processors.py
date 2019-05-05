from django.conf import settings # import the settings file

def static_media(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'EVENT_LOGO_URL': settings.EVENT_LOGO,
            'HOST_LOGO_URL': settings.HOST_LOGO,
            'SPONSOR_LOGO_URL': settings.SPONSOR_LOGO}