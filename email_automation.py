import os
import schedule
from datetime import datetime
import time
import smtplib
from email.message import EmailMessage
from decouple import config


def send_email_with_attachement(sender, recipient, subject, body, file_path, log_file_path):

    """
    this function uses the email library, specifically the EmailMessage class to construct the email.
    It does this is by creating an email object with multiple part that we can manipulate using methods of the EmailMessage instance.
    For example the body part will be added using the add_alternative method, because we are using html.
    The attachement part is handled with the add_attachement method.

    For email sending we use smtplib with the SMTP class that creates an smtp object that will handle;
    Server connection
    Mail sending
    Server closing
    """
    
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject



    # Include the html message in the email
    msg.add_alternative(body, subtype="html")


    # attach the file to the email
    # we use the os library open function instead of the built in function
    file = os.open(file_path, os.O_RDONLY)
    msg.add_attachment(os.read(file, 20), maintype="text", subtype="plain")
    os.close(file)

    # log file
    log_file = os.open(log_file_path, os.O_WRONLY | os.O_APPEND | os.O_CREAT)
    
    # smtp server used to send the email we use mailtrap to test the application
    smtp_server = "sandbox.smtp.mailtrap.io"
    smtp_port = 587

    
    # credentials used to connect to server
    username = config("USERNAME")
    password = config("PASSWORD")
    
    
    # setup the smtp server and send the email
    now = datetime.now()
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() # uses Tls for more secured email
        server.login(username, password)
        

        # send the email
        server.send_message(msg)


        # quit the server
        server.quit()
        
        # writing to the log message
        log_message = f"{now}: Email sent to {recipient}".encode('utf-8')
        os.write(log_file, log_message)
        print("Email with attachment and HTML body sent successfully!")
    
    
    except Exception as e:
        log_message = f"{now}: An error occured when sending an email to {recipient}, {e}".encode('utf-8')
        os.write(log_file, log_message)
        print("An error occured whule sending the message", e)


    finally:
        os.close(log_file)

# Usage example:
sender_email = "admin@admin.com"
recipients_emails = ["recipient1@gmail.com", "recipient2@gmail.com", "recipient3@gmail.com"]
subject = "Test Email with Attachment and HTML Body"
body_html = "<h1>This is a test email with an HTML body sent using Python!</h1>"
attachment_path = "demofile.txt"
log_file_path = "log.txt"


def send_to_all_recipients(sender_email, subject, body_html, attachment_path, log_file_path):
    """
    this function will call send_email_with_attachement for all recipients
    """
    for recipient_email in recipients_emails:
        send_email_with_attachement(sender_email, recipient_email, subject, body_html, attachment_path, log_file_path)




# we schedule the send_to_all_recipients every
schedule.every().day.at("10:30").do(send_to_all_recipients, sender_email, subject, body_html, attachment_path, log_file_path)


# we keep the loop running to check for pending schedules
while True:
    schedule.run_pending()
    time.sleep(1)
