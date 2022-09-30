from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
import jpegdec
from time import sleep
from pimoroni import RGBLED, Button
import gc

gc.collect()

display = PicoGraphics(DISPLAY_PICO_DISPLAY_2, rotate=180)
WIDTH, HEIGHT = display.get_bounds()

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

EYES = 'eyes.jpg'
RIGHT = 'right.jpg'

def draw_jpg(display, filename):
    j = jpegdec.JPEG(display)

    # Open the JPEG file
    j.open_file(filename)

    WIDTH, HEIGHT = display.get_bounds()
    display.set_clip(0, 0, WIDTH, HEIGHT)
    print(f'width: {WIDTH}, height: {HEIGHT}')

    # Decode the JPEG
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
    display.remove_clip()
    display.update()

toggle = False
while True or KeyboardInterrupt:
    if toggle:
        face = RIGHT
        toggle = False
    else:
        face = EYES
        toggle = True
    if button_x.read():
        box.down()
    if button_y.read():
        box.up()
    draw_jpg(display, face)
    sleep(1)