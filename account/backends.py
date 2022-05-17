from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDeniede
from django.utils.module_loading import import_string
from django.utils.translation import LANGUAGE_SESSION_KEY

class CaseInsensitiveModelBackends(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(**{case_insensitive_username_field: username})
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
                
    def user_can_authenticate(self, user):
        return True            


def load_backend(path):
    return import_string(path)()


def _get_backends(return_tuples=False):
    backends = []
    print(backends)
    for backend_path in settings.AUTHENTICATION_BACKENDS:
        backend = load_backend(backend_path)
        backends.append((backend, backend_path) if return_tuples else backend)
    if not backends:
        raise ImproperlyConfigured(
            'No authentication backends have been defined. Does '
            'AUTHENTICATION_BACKENDS contain anything?'
        )
    return backends
