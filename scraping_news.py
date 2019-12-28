import urllib.request
from inscriptis import get_text
import smtplib
import config
import time

def eliminarAcentos(cadena):

    d = {    '\xc1':'A',
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
        nueva_cadena = nueva_cadena.replace(c,d[c])

    auxiliar = nueva_cadena.encode('utf-8')
    return nueva_cadena

def send_email(subject,msg):
    server = smtplib.SMTP(host = 'smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(config.EMAIL_ADDRESS,config.PASSWORD)
    message = "Subject: {} \n\n{}".format(subject,msg)
    print(message)
    server.sendmail(config.EMAIL_ADDRESS,config.EMAIL_SEND1,message)

    server.close()
    print("Successfuly sent")

def obtain_news(url,key_word):
    html = urllib.request.urlopen(url).read().decode('utf-8')
    text = get_text(html)
    texts = text.split("\n\n")
    news = []
    
    for div in texts:
        if key_word in div:
            news.append(div)
    return news

def main():
    url = "https://www.eleconomista.es/"
    key_word = "SUV"

    news = obtain_news(url,key_word)
    subject = 'Pyton has found the following news:'
    msg = "\n\n".join(news)
    msg = eliminarAcentos(msg)

    f = open('last_news.txt','r')
    if f.read() != msg and msg:
        send_email(subject,msg)
        f.close()
        f = open('last_news.txt','w')
        f.write(msg)
        f.close()
    elif not msg:
        print("Nothing found")
    
while True:
    main()
    time.sleep(20)
    
            
        
        


        
