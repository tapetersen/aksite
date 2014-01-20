import settings

def should_show_toolbar(request):
    return request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS \
        or hasattr(request.user, "email") and request.user.email in [a[1] for a in settings.ADMINS]
