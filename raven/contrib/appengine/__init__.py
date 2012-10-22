from google.appengine.api.app_identity import get_default_version_hostname
from raven.base import Client
from raven.contrib.appengine.utils import get_data_from_request


class Sentry(object):
    """
    Google App Engine application for Sentry, when using webapp2.

    Lookup configuration from config.py via SENTRY prop, for example:

    SENTRY = {
        'dsn': 'xxxx',
        'name': 'name',
    }

    Usage:

    >>> import config
    >>> import raven.contrib.appengine import Sentry
    >>> sentry = Sentry(config)
    >>> sentry.capture_exception(request=self.request, exc_info=sys.exc_info())

    Enable/Disable Sentry based on your deployment environment:
    >>> import raven.contrib.appengin.utils import is_enabled
    >>> sentry = Sentry(config, is_enabled=is_enabled(config))

    Since GAE doesn't have access to the socket module, if the name is
    not provided we will default to get_default_version_hostname() from
    the app_identity module.  This returns something like so:

        your_app_id.appspot.com.

    For further information see:

    https://developers.google.com/appengine/docs/python/appidentity/functions

    By default, the client is enabled to send messages to Sentry.  For
    convience there is a utiltiy function
    ``raven.contrib.appengine.utils.is_enabled`` that you can use to
    enable/disable the client while developing locally.
    """
    def __init__(self, config, client_cls=Client, is_enabled=True):
        self.client = None

        if is_enabled:
            self.client = client_cls(
                dsn=config.SENTRY.get('dsn'),
                name=config.SENTRY.get('name', get_default_version_hostname()),
                servers=config.SENTRY.get('sentry_servers'),
                key=config.SENTRY.get('sentry_key'),
                public_key=config.SENTRY.get('public_key'),
                secret_key=config.SENTRY.get('secret_key'),
                project=config.SENTRY.get('project'),
                site=config.SENTRY.get('site'),
                include_paths=config.SENTRY.get('include_paths'),
                exclude_paths=config.SENTRY.get('exclude_paths')
            )

    def capture_exception(self, *args, **kwargs):
        if not self.client:
            return

        request = kwargs.get('request', None)
        data = kwargs.get('data', {})

        if request:
            data.update(get_data_from_request(request))


        return self.client.captureException(exc_info=kwargs.get('exc_info'),
            data=data)

    def capture_message(self, message, **kwargs):
        if not self.client:
            return

        return self.client.captureMessage(message, **kwargs)

