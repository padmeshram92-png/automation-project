import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.utils.logger import log_info, log_error
from backend.services.api_key_manager import get_api_key


class EmailIntegration:
    """Email integration class for sending emails"""

    def __init__(self, smtp_server="smtp.gmail.com", port=587, sender_email=None, password=None):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email or get_api_key("email_sender")
        self.password = password or get_api_key("email_password")

    def send(self, receiver_email: str, subject: str, message: str):
        """
        Send an email

        Args:
            receiver_email: Recipient email address
            subject: Email subject
            message: Email body

        Returns:
            Dictionary with status and message
        """
        try:
            if not self.sender_email or not self.password:
                return {
                    "status": "error",
                    "message": "Email credentials not configured. Please set email_sender and email_password API keys."
                }

            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = receiver_email
            msg["Subject"] = subject

            msg.attach(MIMEText(message, "plain"))

            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.send_message(msg)
            server.quit()

            log_info(f"Email sent to {receiver_email}")
            return {
                "status": "success",
                "message": "Email sent successfully"
            }

        except Exception as e:
            log_error(f"Error sending email: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }


# Default email integration instance
# Uses API keys automatically
default_email_service = EmailIntegration()


def send_email_action(to: str, subject: str = "Automation Result", message: str = ""):
    """
    Wrapper function to send email

    Args:
        to: Recipient email address
        subject: Email subject
        message: Email body

    Returns:
        Result of email sending
    """
    if not to:
        return {
            "status": "error",
            "message": "Recipient email not provided"
        }

    return default_email_service.send(to, subject, message)


def configure_email_integration(sender_email: str, password: str, smtp_server: str = "smtp.gmail.com", port: int = 587):
    """
    Configure email integration with API keys

    Args:
        sender_email: Sender email address
        password: Email password/app password
        smtp_server: SMTP server (default Gmail)
        port: SMTP port (default 587)
    """
    from backend.services.api_key_manager import set_api_key

    set_api_key("email_sender", sender_email)
    set_api_key("email_password", password)
    set_api_key("email_smtp_server", smtp_server)
    set_api_key("email_smtp_port", str(port))

    log_info("Email integration configured successfully")


def test_email_integration(test_email: str):
    """
    Test email integration by sending a test email

    Args:
        test_email: Email address to send test to

    Returns:
        Test result
    """
    return send_email_action(
        to=test_email,
        subject="Email Integration Test",
        message="This is a test email from your automation system. If you received this, email integration is working correctly!"
    )
