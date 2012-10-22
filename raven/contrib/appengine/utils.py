import os

def is_enabled(config):
    """
    Determine whether or not Sentry is currently enabled.

    Check the ``SERVER_SOFTWARE`` environment variable and
    enable sentry if deployed to appspot, otherwise disable.
    :param config: GAE config
    :return: boolean
    """
    if 'Google App Engine' in os.getenv('SERVER_SOFTWARE', ''):
        return True

    return False


def get_data_from_request(request):
    """
    Convenience function to create data from a webapp2 request object.
    :param request:
    :return: dict
    """
    return {
        'sentry.interfaces.Http': {
            'method': request.method,
            'url': request.path_url,
            'query_string': request.query_string,
            'headers': dict(request.headers),
            'env': dict((
                ('REMOTE_ADDR', request.environ['REMOTE_ADDR']),
                ('SERVER_NAME', request.environ['SERVER_NAME']),
                ('SERVER_PORT', request.environ['SERVER_PORT']),
                )),
            }
    }
