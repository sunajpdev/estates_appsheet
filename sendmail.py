from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import os
import smtplib
import configparser

# 環境設定読み込み
ini = configparser.ConfigParser()
ini.read("config.ini", encoding="utf-8")

MAIL_ADDRESS = ini["MAIL"]["MailAddress"]
MAIL_PASS = ini["MAIL"]["MailPass"]
LOG_FILE = ini["LOG"]["DefaultLog"]

# メッセージの作成 htmlmail
def create_message(from_addr, to_addr, subject, body, filename=""):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.attach(MIMEText(body, "html"))
    # 添付ファイル処理
    if filename:
        with open(filename, "rb") as f:
            mb = MIMEApplication(f.read())
        mb.add_header("Content-Disposition", "attachment", filename=filename)
        msg.attach(mb)
    return msg


# メールの送信
def send_mail(msg):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(MAIL_ADDRESS, MAIL_PASS)
        server.send_message(msg)


if __name__ == "__main__":

    filename = LOG_FILE
    if os.path.exists(filename):
        with open(filename, "r") as f:
            body = f.read()
    else:
        body = ""

    title = "Estatesおしらせ"
    msg = create_message(MAIL_ADDRESS, MAIL_ADDRESS, title, body)
    send_mail(msg)
