import hashlib

from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

def facebook_login(request):
    params = _verify_signature(request.COOKIES)
    if params:
        user = authenticate(uid=params['user'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL, {}, ())
            else:
                # Disabled account, pass for now
                pass
        else:
            # Invalid user, pass for now
            pass
    elif request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL, {}, ())
    else:
        return redirect('/', {}, ())

def _verify_signature(cookies):
    api_key = settings.FACEBOOK_API_KEY
    key_prefix = api_key + '_'
    params = dict()
    signature = ''

    for key in sorted(cookies):
        if key.startswith(key_prefix):
            k = key.replace(key_prefix, '')
            v = cookies[key]
            params[k] = v
            signature += '%s=%s' % (k, v)

    hashed = hashlib.md5(signature)
    hashed.update(settings.FACEBOOK_SECRET_KEY)

    if hashed.hexdigest() == cookies[api_key]:
        return params
    else:
        return False