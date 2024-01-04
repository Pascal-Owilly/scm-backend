from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.message import sanitize_address
from google.auth import exceptions, transport, impersonated_credentials

from google.oauth2 import service_account  
from google.auth.transport import requests
from smtplib import SMTP, SMTPAuthenticationError  # Use SMTPAuthenticationError instead
from smtplib import SMTP_SSL as SMTP_SSL  # Import SMTP_SSL

import base64
import os

class OAuthEmailBackend(EmailBackend):
    def open(self):
        # Use SMTP_SSL if secure connection is needed, otherwise use SMTP
        if self.use_ssl:
            self.connection = SMTP_SSL(self.host, self.port, timeout=self.timeout)
        else:
            self.connection = SMTP(self.host, self.port, timeout=self.timeout)

        self.connection.set_debuglevel(1)
        self.connection.ehlo()

        if not self.use_ssl:  # Start TLS only if not using SSL
            self.connection.starttls()
            self.connection.ehlo()

        try:
            # Use OAuth 2.0 for authentication
            target_principal = 'pascalouma54@gmail.com'  # Replace with your Gmail address
            credentials = service_account.Credentials.from_service_account_file(
                os.path.join(os.path.dirname(__file__), 'credentials.json'),
                target_principal=target_principal,
                target_scopes=['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.send']
            )
            credentials.refresh(requests.Request())
        except exceptions.GoogleAuthError as e:
            # Raise SMTPAuthenticationError with a custom error message
                raise SMTPAuthenticationError(535, f'Error authenticating with Gmail: {e}')

        auth_string = 'user={}\1\1auth=Bearer {}'.format(
            sanitize_address(target_principal), credentials.token
        )

        try:
            self.connection.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(auth_string.encode()).decode())
        except SMTPAuthenticationError as e:
            # Raise the exception with a custom error message
            raise SMTPAuthenticationError(f'Error authenticating with Gmail: {e}')

        return self.connection
