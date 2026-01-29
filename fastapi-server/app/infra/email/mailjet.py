from mailjet_rest import Client
from app.core.logger import get_logger
from app.core.config import settings
from app.core.templates import email 


logger = get_logger(__name__)

class EmailService:
    def __init__(self) -> None:
        self.client = Client(
            auth=(
                settings.MAILJET_API_KEY,
                settings.MAILJET_SECRET_KEY,
            ),
            version="v3.1",
        )

        self.sender = {
            "Email": settings.MAILJET_SENDER_EMAIL,
            "Name": "KinetikPod",
        }

    def send_verification_email(self, to_email: str, verification_token: str):
        html_content = email.VERIFICATION_EMAIL_TEMPLATE.format(
            verificationCode=verification_token
        )
        self._send_email(to_email, "Verify your email", html_content)

    def send_welcome_email(self, to_email: str, user_name: str):
        html_content = email.WELCOME_EMAIL_TEMPLATE.format(userName=user_name)
        self._send_email(to_email, "Welcome to KinetikPod!", html_content)

    def send_password_reset_email(self, to_email: str, reset_link: str):
        html_content = email.PASSWORD_RESET_REQUEST_TEMPLATE.format(
            resetLink=reset_link
        )
        self._send_email(to_email, "Reset your password", html_content)

    def send_reset_success_email(self, to_email: str, user_name: str):
        html_content = email.PASSWORD_RESET_SUCCESS_TEMPLATE.format(userName=user_name)
        self._send_email(to_email, "Password Reset Successful", html_content)

    def _send_email(self, to_email: str, subject: str, html_content: str):
        message = {
            "Messages": [
                {
                    "From": self.sender,
                    "To": [{"Email": to_email}],
                    "Subject": subject,
                    "HTMLPart": html_content,
                }
            ]
        }
        try:
            result = self.client.send.create(data=message)
            logger.info(
                f"[EmailService] Email '{subject}' sent to {to_email}:",
                result.status_code,
            )
        except Exception as e:
            logger.error(
                f"[EmailService] Failed to send email '{subject}' to {to_email}:",
                str(e),
            )
            raise


# email_service = EmailService()

