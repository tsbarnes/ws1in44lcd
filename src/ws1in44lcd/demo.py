# -*- coding:utf-8 -*-
from ws1in44lcd import LCD
from ws1in44lcd import keys

import os.path

from inspect import currentframe, getframeinfo
from pathlib import Path
from PIL import Image, ImageDraw


class Demo:
    display: LCD.LCD = None
    lcd_scan_dir: int = LCD.SCAN_DIR_DFT
    width: int = 128
    height: int = 128
    image: Image = None

    def __init__(self):
        # Initialize buttons
        keys.init()

        # 240x240 display with hardware SPI:
        self.display = LCD.LCD()
        self.display.init(self.lcd_scan_dir)
        self.display.clear()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.image = Image.new('RGB', (self.width, self.height))

        # Push the image to the display
        self.display.show_image(self.image)

    def run(self):
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(self.image)

        # Draw the Raspberry Pi logo
        filename = getframeinfo(currentframe()).filename
        parent = Path(filename).resolve().parent
        logo = Image.open(os.path.join(parent, 'raspberry-pi.png'))
        self.image.paste(logo, box=(39, 64))

        # Push the image to the display
        self.display.show_image(self.image)

        while 1:
            # with canvas(device) as draw:
            if keys.get_input(keys.KEY_UP_PIN) == 0:  # button is released
                draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0xff00)  # Up
            else:  # button is pressed:
                draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  # Up filled

            if keys.get_input(keys.KEY_LEFT_PIN) == 0:  # button is released
                draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0xff00)  # left
            else:  # button is pressed:
                draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  # left filled

            if keys.get_input(keys.KEY_RIGHT_PIN) == 0:  # button is released
                draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0xff00)  # right
            else:  # button is pressed:
                draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0)  # right filled

            if keys.get_input(keys.KEY_DOWN_PIN) == 0:  # button is released
                draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0xff00)  # down
            else:  # button is pressed:
                draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0)  # down filled

            if keys.get_input(keys.KEY_PRESS_PIN) == 0:  # button is released
                draw.rectangle((20, 22, 40, 40), outline=255, fill=0xff00)  # center
            else:  # button is pressed:
                draw.rectangle((20, 22, 40, 40), outline=255, fill=0)  # center filled

            if keys.get_input(keys.KEY1_PIN) == 0:  # button is released
                draw.ellipse((70, 0, 90, 20), outline=255, fill=0xff00)  # A button
            else:  # button is pressed:
                draw.ellipse((70, 0, 90, 20), outline=255, fill=0)  # A button filled

            if keys.get_input(keys.KEY2_PIN) == 0:  # button is released
                draw.ellipse((100, 20, 120, 40), outline=255, fill=0xff00)  # B button]
            else:  # button is pressed:
                draw.ellipse((100, 20, 120, 40), outline=255, fill=0)  # B button filled

            if keys.get_input(keys.KEY3_PIN) == 0:  # button is released
                draw.ellipse((70, 40, 90, 60), outline=255, fill=0xff00)  # A button
            else:  # button is pressed:
                draw.ellipse((70, 40, 90, 60), outline=255, fill=0)  # A button filled
            self.display.show_image(self.image)


if __name__ == '__main__':
    demo = Demo()
    demo.run()
