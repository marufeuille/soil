from bluepy import btle
import binascii
from datetime import datetime
import sqlite3

class MyDelegate(btle.DefaultDelegate):
    def __init__(self, addr):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here
        self.addr = addr

    def handleNotification(self, cHandle, data):
        print data
        val = int(binascii.hexlify(data),16)
        print val
        if val > 1000 :
            return
        print val
        conn = sqlite3.connect("humidity.sqlite3")
        cur = conn.cursor();
        cur.execute("insert into data values ('%s', %d, '%s');" % (self.addr, val, datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")))
#        print "insert into data values ('%s', %d, '%s');" % (self.addr, val, datetime.now().strftime("%Y-%m-%dT%H:%m:%SZ"))
        conn.commit()
        conn.close()

p = btle.Peripheral("20:79:35:0A:DB:D5",btle.ADDR_TYPE_PUBLIC,iface="hci0")
p.setDelegate( MyDelegate("20:79:35:0A:DB:D5") )

while True:
    if p.waitForNotifications(60):
        # handleNotification() was called
        continue

    print "Waiting..."
    # Perhaps do something else here
