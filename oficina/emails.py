"""
Module Docstring
"""
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import snoop
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def emails():
    """"""
    smtp_server = "smtp.mailfence.com"
    port = 465
    sender = "micaldas@mailfence.com"
    receiver = "micaldas@gmail.com"
    pwd = "7FsIH1)bP/!3"
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Python Mail Text."
    msg["From"] = sender
    msg["To"] = receiver

    text = """
    I have a very bad feeling about this.
    Any time that I was able to put a email service to work,
    it implied a service and a good deal of time dealing with DNS security and certificates.
    I have my doubts about this 'simple solutions.'
    """
    html = """
    <html>
    <body>
    <p>I have a bad feeling about this.</p>
    <p>Am I repeating myself? It feels as I'm repeating myself.</p>
    </body>
    </html>
    """
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    msg.attach(part1)
    msg.attach(part2)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender, pwd)
            server.sendmail(sender, receiver, msg.as_string())
    except Exception as e:
        print(e)
    # finally:
    #     server.quit()


if __name__ == "__main__":
    emails()
