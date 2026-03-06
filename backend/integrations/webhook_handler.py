import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailIntegration:

    def __init__(self, smtp_server, port, sender_email, password):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.password = password


    def send_email(self, receiver_email, subject, message):

        try:
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

            return {
                "status": "success",
                "message": "Email sent successfully"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }