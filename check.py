import os, sys
import time, datetime
import imaplib
import email
import logging

try:
    from pyfirmata import Arduino, util
except ImportError as e:
    print
    print "Seems like the python firmata library is not installed. Just type: "
    print "$ sudo pip install pyfirmata"
    print "To install it and then try again."
    print
    sys.exit(1)

# @TODO change this for the bit before the @ in your email address, so if your email
# is J.Modaal@artez.nl, just set this variable to J.Modaal
EMAIL_USERNAME = "Jan.Modaal"

def init_arduino():
    # don't forget to change the serial port to suit
    board = pyfirmata.Arduino('/dev/tty.usbmodem26271')
    iter8 = pyfirmata.util.Iterator(board)
    iter8.start()

    # set up pin D9 as Servo Output
    ardpin = board.get_pin('d:9:s')

def move_servo(a):
    ardpin.write(a)

def cb_new_email(subject, timestamp):
    """ This function gets called every time there's a new unread email detected """
    # Hi Gabrielle: this is where you have to put the code
    # that will react to any incoming email.
    # In this case I just print the date and the subject, but you
    # can send a message to your arduino every time.
    print "Received email:", timestamp, "//", subject

def read_passwd():
    """ read you email password form a file called email.secret in your home dir """
    fname = os.path.join(os.path.expanduser("~"), "email.secret")
    print "Trying to read your password from", fname
    with open (fname, "r") as fin:
        data = fin.read().strip()
        return data

def get_unread(mark_as_read=False):
    conn = imaplib.IMAP4_SSL("webmail.artez.nl", 993)
    imap_password = read_passwd()

    # coonect to IAMP mail server
    rv, caps = conn.login(EMAIL_USERNAME, imap_password)
    # list mailboxes
    rv, mboxes = conn.list()
    # select inbox
    rv, mbox = conn.select("Inbox")

    # list all unread emails
    rv, messages = conn.search(None, '(UNSEEN)')
    if rv == 'OK':
        for num in messages[0].split():
            rv, data = conn.fetch(num,'(RFC822)')
            if rv != 'OK':
              print "ERROR getting message", num
              return

            msg = email.message_from_string(data[0][1])
            if not mark_as_read:
                rv, data = conn.store(num,'-FLAGS','\\Seen')
            if rv == 'OK':
                #print data,'\n',30*'-'
                #print msg
                #print 'Message %s: %s' % (num, msg['Subject'])
                #print 'Raw Date:', msg['Date']
                date_tuple = email.utils.parsedate_tz(msg['Date'])
                if date_tuple:
                    local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                    #print "Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S")

                cb_new_email(msg['Subject'], local_date.strftime("%a, %d %b %Y %H:%M:%S"))

    conn.close()


def main():
    try:
        while True:
            get_unread()
            time.sleep(10)
    except KeyboardInterrupt, e:
        logging.info("Seems like you want to exit")
    finally:
        # report before finishing
        logging.info("Finished. Goodbye!")

if __name__ == '__main__':
    #logging.basicConfig(filename="importer.bbcfood.log")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)-15s %(message)s")
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    main()
