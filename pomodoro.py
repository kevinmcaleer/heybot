# pomodoro

from phew import connect_to_wifi, logging
from phew.ntp import fetch
from config import wifi_ssid, wifi_password
import usocket
import jpegdec
import struct
from time import sleep, gmtime, time
from machine import RTC
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
from random import choice
from countdowntimer import CountDownTimer

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=180)

WIDTH, HEIGHT = display.get_bounds()

timer = 1
EYES = 'eyes.jpg'
RIGHT = 'right.jpg'
normal = 1

angry_frames = ['angry01.jpg',
         'angry02.jpg',
         'angry03.jpg',
         'angry04.jpg',
         'angry05.jpg',
         'angry06.jpg',
         'angry07.jpg']

normal_frames = ['normal01.jpg',
                 'normal02.jpg',
                 'normal03.jpg',
                 'normal04.jpg']

static_frames = ['eyes.jpg',
                 'eyes.jpg']
    
RED = display.create_pen(255,0,0)
WHITE = display.create_pen(255,255,255)
BLACK = display.create_pen(0,0,0)
    
class Animate():
    direction = 'forward'
    frame = 1    
    frames = []
    is_done_animating = False
    
    def animate(self, display):
        """ Animate the frames """
        if self.direction == 'forward':
            self.frame += 1
            
            if self.frame > len(self.frames):
                self.direction = 'backward'
                self.frame = len(self.frames)
        else:
            self.frame -= 1
            if self.frame < 1:
                self.direction = 'forward'
                self.frame = 1
                self.is_done_animating = True
        
        draw_jpg(display,self.frames[self.frame-1])

def draw_jpg(display, filename):
    j = jpegdec.JPEG(display)

    # Open the JPEG file
    j.open_file(filename)

    WIDTH, HEIGHT = display.get_bounds()
    display.set_clip(0, 0, WIDTH, HEIGHT)

    # Decode the JPEG
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
    display.remove_clip()

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

def banner(display, bg_colour, fg_colour):
    display.set_pen(bg_colour)
    display.rectangle(0,210,WIDTH,HEIGHT)
    display.set_pen(fg_colour)

draw_jpg(display,EYES)
logging.debug('about to connect to wifi')

connect_to_wifi(wifi_ssid, wifi_password)

t = update_clock()

# Create a countdown timer
countdown = CountDownTimer()
countdown.duration_in_seconds = 3


display.set_font("bitmap8")
current_time = countdown.current_time_str
print(current_time)
x = 1
y = 1
scale = 4
angle = 0
spacing = 1
wordwrap = False
display.set_pen(15)

# Setup Animations
animations = [angry_frames,normal_frames, static_frames]
animation = Animate()
animation.frames = choice(animations)

# Start the timer
countdown.go()

RED = display.create_pen(255,0,0)
while True:
    current_time = countdown.current_time_str
    display.set_pen(0)
    display.clear()
    # draw_jpg(display, EYES)
    #animate_normal(display)
    countdown.tick()
    countdown.status()
    remaining_time = countdown.remaining_str
    
    if not animation.is_done_animating:
        animation.animate(display)
    else:
        animation.frames = choice(animations)
        animation.is_done_animating = False
        animation.animate(display)
    
    display.set_pen(15)
    x = WIDTH // 2 - (display.measure_text(current_time, scale, spacing) //2 )
    display.text(current_time, x, y, wordwrap, scale, angle, spacing)
    
    x = WIDTH // 2 - (display.measure_text(remaining_time, scale, spacing) //2 )
    if countdown.alarm:
        print('countdown done')
        if gmtime()[5] % 2 == 0 :
            banner(display,RED, WHITE)
        else:
            banner(display,BLACK,RED)
    else:
        display.set_pen(RED)
    display.text(remaining_time, x, y+210, wordwrap, scale, angle, spacing)
    
    display.update()
    sleep(0.01)