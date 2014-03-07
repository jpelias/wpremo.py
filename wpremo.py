#sudo apt-get install python-pip
#sudo apt-get install libssl-dev 
#sudo pip install coinkit
#sudo pip install pybitcointools
#sudo pip install scrypt
#sudo pip install passlib

from email.mime.text import MIMEText
import smtplib
import binascii
import pybitcointools as bitcoin
import itertools
import random
import scrypt
import string
import sys
from passlib.utils.pbkdf2 import pbkdf2
from coinkit.keypair import BitcoinKeypair

def id_generator(size=8, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase): return ''.join(random.choice(chars) for x in range(size))

def xor(s1, s2):
    return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

def warp(passphrase, salt=""):
    s1 = _scrypt(passphrase, salt="")
    s2 = _pbkdf2(passphrase, salt="")
    key = binascii.hexlify(xor(s1, s2))
    return key, bitcoin.pubtoaddr(bitcoin.privtopub(key))


def _pbkdf2(passphrase, salt=""):
    return pbkdf2(passphrase + "\x02", salt=salt+"\x02", keylen=32,rounds=65536, prf="hmac-sha256")


def _scrypt(passphrase, salt=""):
    return scrypt.hash(passphrase + "\x01", salt+"\x01", N=262144, r=8, p=1)

def test():
    salt= ""
    premo = id_generator()
    salida = warp(premo,salt)
    addy = salida[1]
    print addy,premo
    if addy == "1AdU3EcimMFN7JLJtceSyrmFYE3gF5ZnGj":
        k = BitcoinKeypair(str(salida[0]))
        print addy, premo, k.wif_pk()
        return premo
 
def enviamail(mensaje):

    addr_to   = 'user@gmail.com'
    addr_from = 'bitcoin@mandrillapp.com'
    smtp_server = 'smtp.mandrillapp.com:587'
    smtp_user   = 'user@gmail.com'
    smtp_pass   = '3upTRMWZxDmaIfrCgmD4sQ'
    msg = MIMEText(mensaje)
    msg['To'] = addr_to
    msg['From'] = addr_from
    msg['Subject'] = '1AdU3EcimMFN7JLJtceSyrmFYE3gF5ZnGj'
    s = smtplib.SMTP(smtp_server)
    s.login(smtp_user,smtp_pass)
    s.sendmail(addr_from, addr_to, msg.as_string())
    s.quit()
    return 

while True:

    mensaje = test()

    if mensaje:
        
        print mensaje
        print "enviamail(mensaje)"
        exit()


