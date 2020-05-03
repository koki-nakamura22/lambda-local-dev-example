# How to execute this file.
# Step 1: Launch a mail server locally.
# docker run --rm -itd -e DEFAULT_REGION="us-east-2" -e SERVICES="ses" -p 4567-4582:4567-4582 -p 8080:8080 localstack/localstack
# 
# Step 2: Executing a Lambda function script file.
# docker run --rm -v "$PWD":/var/task:ro,delegated lambci/lambda:python3.8 lambdas_with_docker.lambda_func_with_ses.lambda_handler

import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
import boto3
from botocore.exceptions import ClientError

# Character code setting
CHARSET = 'UTF-8'

# Sender setting
SENDER = 'test sender <test-sender@test.com>'

# Client setting
CLIENT = boto3.client('ses', region_name='us-east-2', endpoint_url='http://host.docker.internal:4579')
# Authentication settings for sender email address
RECIPIENT = 'test-recipient@test.com'
CLIENT.verify_email_identity(EmailAddress=SENDER)

def lambda_handler(event, context):
    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = 'Test subject'
    msg['From'] = SENDER
    msg['To'] = RECIPIENT

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')

    # Set email bodies.
    # It is also possible to set only one of the two.

    # Set html body.
    body_html = '''
    <html>
        <head></head>
        <body>
            <h1>Test mail</h1>
            <p>This mail was sent by AWS SES.</p>
        </body>
    </html>
    '''
    htmlpart = MIMEText(body_html.encode(CHARSET), 'html', CHARSET)
    msg_body.attach(htmlpart)

    # Set text body.
    body_text = '''
    Test mail
    This mail was sent by AWS SES.
    '''
    textpart = MIMEText(body_text.encode(CHARSET), 'plain', CHARSET)
    msg_body.attach(textpart)

    # Attach files.
    attachment = ['/tmp/test1.pdf', '/tmp/test2.png', '/tmp/test3.txt']
    __createDummyFilesForSendingEmail(attachment)
    for each_attachment in attachment:
        att = MIMEApplication(open(each_attachment, 'rb').read())
        att.add_header('Content-Disposition','attachment',filename=os.path.basename(each_attachment))
        msg.attach(att)

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    # Send the email.
    #Provide the contents of the email.
    response = CLIENT.send_raw_email(
        Source=SENDER,
        Destinations=[
            RECIPIENT
        ],
        RawMessage={
            'Data':msg.as_string(),
        }
    )

    return {
        'statusCode': 200,
        'body': response
    }

def __createDummyFilesForSendingEmail(files):
    import pathlib
    for file in files:
        path = pathlib.Path(file)
        path.touch()
