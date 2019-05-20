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


RABBIT_HOST = getenv('RABBIT_HOST', 'localhost')
RABBIT_PORT = getenv('RABBIT_PORT', 5672)

SMTP_USER, SMTP_PASSWORD = getsec('SMTP_CREDS', 'mailer_smtp').split(':')
print(SMTP_USER, SMTP_PASSWORD)

SMTP_HOST = getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = getenv('SMTP_PORT', 465)
