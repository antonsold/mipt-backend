from os import getenv


def getsec(envname, secname=None, default=None):
    val = getenv(envname)
    if val is None and secname is not None:
        try:
            val = open('/run/secrets/' + secname).read().strip()
        except FileNotFoundError:
            pass
    if val is None:
        val = default
    return val


SECRET_KEY = getsec('SECRET_KEY', 'flask_key')

ACTIVATION_TOKEN_LIFETIME = int(getenv('ACTIVATION_TOKEN_LIFETIME', 60 * 60 * 24))

RABBIT_HOST = getenv('RABBIT_HOST', 'localhost')
RABBIT_PORT = getenv('RABBIT_PORT', 5672)
