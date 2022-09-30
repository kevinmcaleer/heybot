# pomodoro

from phew import connect_to_wifi, logging
from phew.ntp import fetch
from config import wifi_ssid, wifi_password
import usocket
import struct
from time import sleep, gmtime
from machine import RTC
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=180)

timer = 1

def update_clock(max_attempts = 5):
    ntp_host = 'pool.ntp.org'
    attempt = 1
    while attempt < max_attempts:
        try:
            query = bytearray(48)
            query[0] = 0x1b
            address = usocket.getaddrinfo(ntp_host, 123)[0][-1]
            socket = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
            socket.settimeout(30)
            socket.sendto(query, address)
            data = socket.recv(48)
            socket.close()
            local_epoch = 2208988800
            timestamp = struct.unpack("!I", data[40:44])[0] - local_epoch
            t = gmtime(timestamp)
            if not t:
                logging.error(" - failed to fetch time from ntp server")
                return False
            RTC().datetime((t[0], t[1], t[2], t[6],t[3],t[4],t[5],0))
            logging.info(" - rtc synced")
            return True
        except Exception as e:
            logging.error(e)
            
        attempt += 1
    return False

t = update_clock()
print(f't:{t}')

display.set_font("bitmap8")
current_time = 'time'
x = 1
y = 1
scale = 1
angle = 0
spacing = 0
wordwrap = False
display.set_pen(15)
while True:
    display.text(current_time, x, y, wordwrap, scale, angle, spacing)
    display.update()
    sleep(1)