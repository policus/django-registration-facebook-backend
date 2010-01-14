from django.forms import Form
from django.conf import settings

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import AnonymousUser, User

from registration import signals

from facebook_connect.views import _verify_signature
from facebook_connect.models import FacebookProfile

class FacebookConnectBackend(object):
    
    def register(self, request, **kwargs):
        params = _verify_signature(request.COOKIES)
        if params and params['user'] != 'None':
            uid = params['user']
            try:
                profile = FacebookProfile.objects.get(uid=uid)
                user_obj = profile.user
            except FacebookProfile.DoesNotExist:
                # Check that the username is unique, and if so, create a user and profile
                try:
                    existing_user = User.objects.get(username=uid)
                    # Should we redirect here, or return False and redirect in post_registration_redirect?
                    return False
                except User.DoesNotExist:
                    user_obj = User.objects.create(
                        username=uid,
                        email='',
                        password=User.objects.make_random_password(16)
                    )
                    profile = FacebookProfile.objects.create(
                        user=user_obj,
                        uid=uid
                    )
            
            signals.user_registered.send(
                sender=self.__class__,
                user=user_obj,
                request=request
            )
            
            user = authenticate(uid=uid)
            login(request, user)
        elif request.user.is_authenticated():
            user_obj = request.user
        else:
            # Perhaps we should handle this differently?
            user_obj = AnonymousUser()
        return user_obj
    
    def registration_allowed(self, request):
        return getattr(settings, 'REGISTRATION_OPEN', True)
    
    def get_form_class(self, request):
        # Pass back an empty instance of the form class, because we are not using a registration form.
        return Form
    
    def post_registration_redirect(self, request, user):
        if user is False:
            redirect_url = '/'
        else:
            redirect_url = getattr(settings, 'FACEBOOK_POST_REGISTRATION_REDIRECT', settings.LOGIN_REDIRECT_URL)
        return (redirect_url, (), {})
    
    def activate(self, request):
        return NotImplementedError

    def post_activation_redirect(self, request, user):
        return NotImplementedError