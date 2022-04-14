import time
import easyimap as e
import smtplib
import imaplib
import re
import logging
from datetime import date
from selenium import webdriver

code = "ERROR"
pw = "Email password"
user = "Email"
send = False
generator = False #True für wirklich anmelden, False für tests!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
logging.basicConfig(filename=str(date.today()) + ' code.txt', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def delete():
    logging.warning('Email deleted!')
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(user, pw)
    imap.select("INBOX")
    status, message_id_list = imap.search(None, "ALL")
    messages = message_id_list[0].split(b' ')
    print("Deleting mails")
    count =1
    for mail in messages:
        imap.store(mail, "+FLAGS", "\\Deleted")

        print(count, "mail(s) deleted")
        count +=1
    print("All selected mails have been deleted")

    imap.expunge()
    imap.close()
    imap.logout()



def generat(pn, n, t, em, st, z, c, bday):
    print("Process started")

    driver = webdriver.Chrome('./chromedriver.exe')
    mail_text = em
    if generator:
        driver.get("https://gn-schnelltest.de/checkin/")

        time.sleep(5)

        prename = driver.find_element_by_name("prename")
        prename.send_keys(pn)

        name = driver.find_element_by_name("name")
        name.send_keys(n)

        tel = driver.find_element_by_name("tel")
        tel.send_keys(t)

        mail = driver.find_element_by_name("mail")
        mail.send_keys(em)

        mail2 = driver.find_element_by_name("mail2")
        mail2.send_keys(em)

        street = driver.find_element_by_name("street")
        street.send_keys(st)

        zip = driver.find_element_by_name("zip")
        zip.send_keys(z)

        city = driver.find_element_by_name("city")
        city.send_keys(c)

        birthday = driver.find_element_by_name("birthday")
        birthday.send_keys(bday)

        button = driver.find_element_by_xpath("//button[text()='Einchecken']")
        button.click()

        time.sleep(3)

        buttonC = driver.find_element_by_class_name("btn.wide.success")
        buttonC.click()

        time.sleep(3)

        buttonC2 = driver.find_element_by_class_name("btn.wide.success")
        buttonC2.click()

        time.sleep(3)

        buttonC3 = driver.find_element_by_class_name("btn.wide.success")
        buttonC3.click()

        time.sleep(3)

        code2 = driver.find_element_by_class_name("info.success")
        print(code2.text)
        mail_text = code2.text
        time.sleep(4)

    logging.warning(em + ' send request, with code: ' + mail_text)
    RCPT_TO = em
    subject = "Coronatest Registriercode"
    DATA = 'From:%s\nTo:%s\nSubject:%s\n\n%s' % (user, RCPT_TO, subject, mail_text)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(user, pw)
    server.sendmail(user, RCPT_TO, DATA)

    server.quit()
    send = False


def false_sender(em):
    mail_text = "Sorry you not allowed to use it!"
    RCPT_TO = em
    subject = "Coronatest Registriercode"
    DATA = 'From:%s\nTo:%s\nSubject:%s\n\n%s' % (user, RCPT_TO, subject, mail_text)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(user, pw)
    server.sendmail(user, RCPT_TO, DATA)

    server.quit()
    send = False
    logging.error(em + " " + 'send request but not allowed')



server_read = e.connect("imap.gmail.com", user, pw)
if not server_read.listids() == []:
    delete()

while True:
    logging.basicConfig(filename=str(date.today()) + ' code.txt', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    server_read = e.connect("imap.gmail.com", user, pw)
    if not server_read.listids() == []:
        print(server_read.listids())
        email = server_read.mail(server_read.listids()[0])
        print(email.title)
        print("...")
        print(email.from_addr)
        print("...")

        mail = re.search('<(.+?)>', email.from_addr).group(1)

        if email.title == "Anmelden":
            if mail == "Enter allowed Email 1":
                generat("name", "last name", "phone number", "Email", "Street + house number", "postal code", "location", "Date of birth")

            elif mail == "Enter allowed Email 2":
                generat("name", "last name", "phone number", "Email", "Street + house number", "postal code", "location", "Date of birth")

            elif mail == "Enter allowed Email 3":
                generat("name", "last name", "phone number", "Email", "Street + house number", "postal code", "location", "Date of birth")

            elif mail == "Enter allowed Email 4":
                generat("name", "last name", "phone number", "Email", "Street + house number", "postal code", "location", "Date of birth")

            else:
                print("---")
                print(re.search('<(.+?)>', email.from_addr).group(1))
                print("---")
                false_sender(re.search('<(.+?)>', email.from_addr).group(1))

        delete()

#Web automatisirung: https://youtu.be/gRMbCvQgOoU
#E-Mail senden: https://youtu.be/PRiluD-qHFA
#E-Mail lesen: https://youtu.be/Xii4bENJSCw

