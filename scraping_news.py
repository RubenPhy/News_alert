import urllib.request
from inscriptis import get_text
import smtplib
import time
import sys
sys.path.append(r'C:\Users\Ruben\Documents\Inversion\Algoritmos_inversion\News')

import config


def eliminarAcentos(cadena):

    d = {'\xc1':'A',
        '\xc9':'E',
        '\xcd':'I',
        '\xd3':'O',
        '\xda':'U',
        '\xdc':'U',
        '\xd1':'N',
        '\xc7':'C',
        '\xed':'i',
        '\xf3':'o',
        '\xf1':'n',
        '\xe7':'c',
        '\xba':'',
        '\xb0':'',
        '\x3a':'',
        '\xe1':'a',
        '\xe2':'a',
        '\xe3':'a',
        '\xe4':'a',
        '\xe5':'a',
        '\xe8':'e',
        '\xe9':'e',
        '\xea':'e',
        '\xeb':'e',
        '\xec':'i',
        '\xed':'i',
        '\xee':'i',
        '\xef':'i',
        '\xf2':'o',
        '\xf3':'o',
        '\xf4':'o',
        '\xf5':'o',
        '\xf0':'o',
        '\xf9':'u',
        '\xfa':'u',
        '\xfb':'u',
        '\xfc':'u',
        '\xe5':'a'}
    nueva_cadena = cadena
    for c in d.keys():
        nueva_cadena = nueva_cadena.replace(c, d[c])

    return nueva_cadena


def send_email(subject, msg, web, key_word):

    server = smtplib.SMTP(host='smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(config.EMAIL_ADDRESS, config.PASSWORD)
    message = "Subject: {} \n\n{}".format(subject, msg)
    print(message)
    server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_SEND1, message)

    server.close()
    print("Successfully sent the email for the:", web, "with the word:", key_word, '. To the mail')


def get_news(url, key_word):

    html = urllib.request.urlopen(url).read().decode('utf-8')
    text = get_text(html)
    texts = text.split("\n\n")
    news = []
    
    for div in texts:
        if key_word in div:
            news.append(div)
    return news


def check_and_send(f, msg, subject, web, key_word):

    if msg == '':
        print("Nothing found for the web:", web, ' for the word:', key_word)
        return True
    elif f.read() == msg:
        print("Message already sent for the web:", web, ' for the word:', key_word)
    elif f.read() != msg:
        send_email(subject, msg, web, key_word)
        f.write(msg)
        f.close()


def main():
    urls = ["https://www.eleconomista.es/", 'https://www.elconfidencial.com/']
    key_words = ["PSOE"]

    for key_word in key_words:
        for url in urls:

            news = get_news(url, key_word)
            subject = 'Python has found the following news:'
            msg = "\n\n".join(news)
            msg = eliminarAcentos(msg)

            web = url.split('www.')[1].split('.')[0]
            print('Web :', web, ' for the word:', key_word)
            file = web + '_' + key_word + '_last_news.txt'

            try:
                with open(file, 'r+') as f:
                    check_and_send(f, msg, subject, web, key_word)
            except IOError:
                with open(file, 'w'):
                    pass
                with open(file, 'r+') as f:
                    check_and_send(f, msg, subject, web, key_word)


while True:
    main()
    time.sleep(30)