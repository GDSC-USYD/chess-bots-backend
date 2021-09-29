# Email functions to send forgotten password reminder
import smtplib, ssl
import email.message
import os



def send_reminder_email(email_recv, password):
    """
    Sends password reminder to user given -> email_recv, password
    Uses SMTP relay and TLS encryption
    Returns -> email_send_message
    """
    email_send_message = "OK"
    try:

        # get credentials
        email_sender, email_pass, email_port, email_gdsc, smtp_server = get_email_credentials()

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, email_port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(email_sender, email_pass)

            # create message
            message = get_message(email_recv, password, email_gdsc)

            #send email
            server.sendmail(email_sender, email_recv, message)

    except Exception as e:
        print(e)
        email_send_message = str(e)

    return email_send_message



def get_email_credentials():
    """
    Retrieves private email credentials as environment variables.
    Returns -> email_sender, email_pass, email_port, email_gdsc, smtp_server
    """

    # get email credentials
    email_sender = os.environ["EMAIL_SENDER"]
    email_pass = os.environ["EMAIL_PASS"]
    email_port = os.environ.get("EMAIL_PORT", 587)
    email_gdsc = os.environ["EMAIL_GDSC"]
    smtp_server = os.environ["SMTP_SERVER"]

    return email_sender, email_pass, email_port, email_gdsc, smtp_server



def get_message(email_recv, password, email_gdsc):
    """
    Creates password reminder email in HTML format given -> email, password, email_sender
    Returns -> message
    """
    # create message
    msg = email.message.Message()

    msg['Subject'] = "Password Reminder - GDSC USYD's Chess Bots Googlethon!"
    msg['From'] = f'GDSC USYD Chess Bots <{email_gdsc}>'
    msg['To'] = f'Chess Bot Builder... and password forgetter! <{email_recv}>'
    msg.add_header('Content-Type','text/html')
    msg.set_payload(f"""<h1>GDSC USYD's Chess Bots Googlethon!</h1><h1>You've requested a password reminder, your password is...</h1><h3>{password}</h3><b>Try not to forget it again!!</b>""")

    return msg.as_string()
