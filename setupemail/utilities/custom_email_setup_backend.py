from django.core.mail.backends.smtp import EmailBackend
from ..models import EmailSetup

class CustomEmailBackend(EmailBackend):
    def __init__(self, **kwargs):
        email_setup = EmailSetup.objects.first()  # Assuming you have only one setup
        if email_setup:
            kwargs['host'] = email_setup.smtp_server_address
            kwargs['port'] = email_setup.port
            kwargs['username'] = email_setup.smtp_username or email_setup.email_address
            kwargs['password'] = email_setup.password
            kwargs['use_tls'] = email_setup.security == 'TSL'
            kwargs['use_ssl'] = email_setup.security == 'SSL'
            kwargs['fail_silently'] = False
        super().__init__(**kwargs)
