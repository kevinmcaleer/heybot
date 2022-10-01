# pomodoro

from phew import connect_to_wifi, logging
from phew.ntp import fetch
from config import wifi_ssid, wifi_password
import usocket
import jpegdec
import struct
from time import sleep, gmtime
from machine import RTC
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=180)

timer = 1
EYES = 'eyes.jpg'
RIGHT = 'right.jpg'

def draw_jpg(display, filename):
    j = jpegdec.JPEG(display)

    # Open the JPEG file
    j.open_file(filename)

    WIDTH, HEIGHT = display.get_bounds()
    display.set_clip(0, 0, WIDTH, HEIGHT)

    # Decode the JPEG
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
    display.remove_clip()
    display.update()

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

def get_time():
    t = machine.RTC()
    year = t.datetime()[0]
    month = t.datetime()[1]
    day = t.datetime()[2]
    hour = t.datetime()[4]
    minute = t.datetime()[5] 
    second = t.datetime()[6]
    h = str(hour)
    m = str(minute)
    s = str(second)
    t_str = f"{h:02}:{m:02}:{s:02}"
    return t_str



draw_jpg(display,EYES)
logging.debug('about to connect to wifi')

connect_to_wifi(wifi_ssid, wifi_password)

t = update_clock()

display.set_font("bitmap8")
current_time = get_time()
print(current_time)
x = 1
y = 1
scale = 4
angle = 0
spacing = 1
wordwrap = False
display.set_pen(15)
while True:
    current_time = get_time()
    display.set_pen(0)
    display.clear()
    draw_jpg(display, EYES)
    display.set_pen(15)
    display.text(current_time, x, y, wordwrap, scale, angle, spacing)
    
    display.update()
    sleep(1)