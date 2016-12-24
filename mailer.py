#!/usr/bin/env python
import argparse
import subprocess
import tempfile
import smtplib
import email.mime.multipart
from email.MIMEText import MIMEText
import logging


def set_log():
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    fm = logging.Formatter('%(filename)s [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')

    console = logging.StreamHandler()
    console.setLevel(LOG_LEVEL)
    console.setFormatter(fm)

    logger.addHandler(console)


def get_body_msg():
    logging.info("[!] Opening vim to write the body ..")
    tmp = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    tmp_name = tmp.name
    tmp.close()
    subprocess.call(['vim', tmp_name])

    with open(tmp_name) as body_:
        body_ = body_.read()

    return body_


def send(server, port, sender, to, reply_to, subject, body, priority):
    msg = email.mime.multipart.MIMEMultipart()
    msg['to'] = to
    msg['from'] = sender
    msg['subject'] = subject
    msg['X-Priority'] = priority
    msg.add_header('reply-to', reply_to)

    server = smtplib.SMTP(server, int(port))
    msg.attach(MIMEText(body))
    server.sendmail(sender, to, msg.as_string())
    server.close()


def parse_args():
    parser = argparse.ArgumentParser(description='Send spoofed email message')

    parser.add_argument('--server', type=str,
                        help='SMTP Server (default localhost)', default="localhost")
    parser.add_argument('--port', type=int,
                        help='SMTP Port (defaut 25)', default=25)
    parser.add_argument('--sender', type=str,
                        help='Sender -> from who we send email', required=True)
    parser.add_argument('--to', type=str,
                        help='Receiver-> to who we send email', required=True)
    parser.add_argument('--priority', type=int,
                        help='Message priority (default 3)', default=3)
    parser.add_argument('--reply-to', type=str, help='Reply-To', required=True)
    parser.add_argument('--subject', type=str, help='Message subject', required=True)

    return parser.parse_args()


if __name__ == '__main__':
    LOG_LEVEL = 'INFO'   # 'DEBUG'
    set_log()

    config = parse_args()

    msg_body = get_body_msg
    try:
        send(config.server, config.port, config.sender, config.to,
             config.reply_to, config.subject, msg_body, config.priority)
        logging.info("[-] E-mail successfully spoofed.")
    except Exception as e:
        exit('Error: %s' % e)
