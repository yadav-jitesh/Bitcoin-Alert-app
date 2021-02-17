import requests
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import getpass


def send_email():
    # msg object to hold the msg blueprint
    msg = MIMEMultipart()

    # the breakdown for the email headers field, password field, to field, from field and subject body
    password = user_password
    msg['From'] = user_email
    msg['To'] = send_to
    msg['Subject'] = "Bitcoin price Alert!"

    # your message
    message = "Hello " + user_name + "\nBitcoin Alert, price of bitcoin is " + str(
        bitcoin_rate) + ". better make move.\nRegards,\n" + user_name

    # adds in the message from the above variable
    msg.attach(MIMEText(message, 'plain'))

    # initialize the gmail server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the email
    server.login(msg['From'], password)

    # sends the message
    server.sendmail(msg['From'], msg['To'], message)

    server.quit()

    # for debugging prints to your console
    print("successfully sent email to %s:" % (msg['To']))
    print("Price of bitcoin was at " + str(bitcoin_rate))


user_name = input('Enter name: ')
user_email = input('Enter your gmail address: ')
user_password = getpass.getpass()
send_to = input('Enter email address to send to: ')
threshold_value = input('Alert if Bitcoin drops below: ')

while True:
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = requests.get(
        url,
        headers={"Accept": "application/json"},
    )
    data = response.json()
    bpi = data['bpi']
    USD = bpi['USD']
    bitcoin_rate = int(USD['rate_float'])
    if bitcoin_rate < int(threshold_value):
        send_email()
        print('system will check for price again in 4 minutes. Ctrl + C to quit.')
        time.sleep(120)
    else:
        time.sleep(300)
        print('Bitcoin rate ' + str(bitcoin_rate) + '. Will check price again in 5 minutes. Ctrl + C to quit.')
