# skipped your comments for readability
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Source email (that one from who the email will be sent)
class Sender:
    def __init__(self, data):
        self.email = data["email"]
        self.password = data["password"]

# Target email (that one to who the email will be sent)
class Target:
    def __init__(self, data):
        self.email = data["email"]

# Email content
class Email:
    def __init__(self, data):
        try:
            self.subject = data["subject"]
            self.content = data["content"]

            if (self.subject == "" or self.content == ""):
                raise Exception("email subject or content invalid")

        except Exception as error:
            print("an error occurred in email content building")
            print(error)
            sys.exit(1)


# Main class
class SendEmail:
    def __init__(self, data):
        self.sender = data["sender"]
        self.target = data["target"]
        self.email = data["email"]

        self.server = None
        self.msg = None

    # configure what smtp server to use
    def serverConfigurations(self):
        self.server = smtplib.SMTP_SSL('smtp.gmail.com')

    # execute the login
    def login(self):
        try:
            self.server.login(self.sender.email, r""+ self.sender.password +"")
        except Exception as error:
            print("An error occurred in login")
            print(error)
            sys.exit(1)

    # email content construction
    def buildEmailContent(self):
        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = self.email.subject
        self.msg['From'] = self.sender.email
        self.msg['To'] = self.target.email
        emailsBody = MIMEText(self.email.content, 'html')
        self.msg.attach(emailsBody)

    # the email sending itself
    def send(self):
        self.serverConfigurations()
        self.login()
        self.buildEmailContent()
        try:
            self.server.sendmail(self.sender.email, self.target.email, self.msg.as_string())
            self.server.quit()
            print("email is sent correctly")
            return True
        except Exception as error:
            print("An error occurred")
            print(error)
            

sender = Sender({ "email":"<YOUR_GMAIL>", "password": "<YOUR_PASSWORD>" })
target = Target({ "email": "<YOUR_EMAIL_TARGET>" })
email = Email({ "subject": "<EMAIL_SUBJECT>", "content": "<EMAIL_CONTENT>" })
emailSending = SendEmail({ "sender": sender, "target": target, "email": email})
emailSending.send()
