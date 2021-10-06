# -*- coding:UTF-8 -*-
from ws1in44lcd import config

import RPi.GPIO as GPIO
import numpy as np


LCD_1IN44 = 1
LCD_WIDTH = 128
LCD_HEIGHT = 128
LCD_X = 2
LCD_Y = 1

LCD_X_MAX_PIXEL = 132
LCD_Y_MAX_PIXEL = 162

# scanning method
L2R_U2D = 1
L2R_D2U = 2
R2L_U2D = 3
R2L_D2U = 4
U2D_L2R = 5
U2D_R2L = 6
D2U_L2R = 7
D2U_R2L = 8
SCAN_DIR_DFT = U2D_R2L


class LCD:
    """
    This class provides access to the LCD screen
    """
    def __init__(self):
        self.width = LCD_WIDTH
        self.height = LCD_HEIGHT
        self.LCD_Scan_Dir = SCAN_DIR_DFT
        self.LCD_X_Adjust = LCD_X
        self.LCD_Y_Adjust = LCD_Y

    @staticmethod
    def reset():
        GPIO.output(config.LCD_RST_PIN, GPIO.HIGH)
        config.driver_delay_ms(100)
        GPIO.output(config.LCD_RST_PIN, GPIO.LOW)
        config.driver_delay_ms(100)
        GPIO.output(config.LCD_RST_PIN, GPIO.HIGH)
        config.driver_delay_ms(100)

    @staticmethod
    def write_register(register):
        GPIO.output(config.LCD_DC_PIN, GPIO.LOW)
        config.spi_write_byte([register])

    @staticmethod
    def write_data_8bit(data):
        GPIO.output(config.LCD_DC_PIN, GPIO.HIGH)
        config.spi_write_byte([data])

    @staticmethod
    def write_data_nlen16bit(data, data_len):
        GPIO.output(config.LCD_DC_PIN, GPIO.HIGH)
        for i in range(0, data_len):
            config.spi_write_byte([data >> 8])
            config.spi_write_byte([data & 0xff])

    def init_register(self):
        # ST7735R Frame Rate
        self.write_register(0xB1)
        self.write_data_8bit(0x01)
        self.write_data_8bit(0x2C)
        self.write_data_8bit(0x2D)

        self.write_register(0xB2)
        self.write_data_8bit(0x01)
        self.write_data_8bit(0x2C)
        self.write_data_8bit(0x2D)

        self.write_register(0xB3)
        self.write_data_8bit(0x01)
        self.write_data_8bit(0x2C)
        self.write_data_8bit(0x2D)
        self.write_data_8bit(0x01)
        self.write_data_8bit(0x2C)
        self.write_data_8bit(0x2D)

        # Column inversion
        self.write_register(0xB4)
        self.write_data_8bit(0x07)

        # ST7735R Power Sequence
        self.write_register(0xC0)
        self.write_data_8bit(0xA2)
        self.write_data_8bit(0x02)
        self.write_data_8bit(0x84)
        self.write_register(0xC1)
        self.write_data_8bit(0xC5)

        self.write_register(0xC2)
        self.write_data_8bit(0x0A)
        self.write_data_8bit(0x00)

        self.write_register(0xC3)
        self.write_data_8bit(0x8A)
        self.write_data_8bit(0x2A)
        self.write_register(0xC4)
        self.write_data_8bit(0x8A)
        self.write_data_8bit(0xEE)

        self.write_register(0xC5)
        self.write_data_8bit(0x0E)

        # ST7735R Gamma Sequence
        self.write_register(0xe0)
        self.write_data_8bit(0x0f)
        self.write_data_8bit(0x1a)
        self.write_data_8bit(0x0f)
        self.write_data_8bit(0x18)
        self.write_data_8bit(0x2f)
        self.write_data_8bit(0x28)
        self.write_data_8bit(0x20)
        self.write_data_8bit(0x22)
        self.write_data_8bit(0x1f)
        self.write_data_8bit(0x1b)
        self.write_data_8bit(0x23)
        self.write_data_8bit(0x37)
        self.write_data_8bit(0x00)
        self.write_data_8bit(0x07)
        self.write_data_8bit(0x02)
        self.write_data_8bit(0x10)

        self.write_register(0xe1)
        self.write_data_8bit(0x0f)
        self.write_data_8bit(0x1b)
        self.write_data_8bit(0x0f)
        self.write_data_8bit(0x17)
        self.write_data_8bit(0x33)
        self.write_data_8bit(0x2c)
        self.write_data_8bit(0x29)
        self.write_data_8bit(0x2e)
        self.write_data_8bit(0x30)
        self.write_data_8bit(0x30)
        self.write_data_8bit(0x39)
        self.write_data_8bit(0x3f)
        self.write_data_8bit(0x00)
        self.write_data_8bit(0x07)
        self.write_data_8bit(0x03)
        self.write_data_8bit(0x10)

        # Enable test command
        self.write_register(0xF0)
        self.write_data_8bit(0x01)

        # Disable ram power save mode
        self.write_register(0xF6)
        self.write_data_8bit(0x00)

        # 65k mode
        self.write_register(0x3A)
        self.write_data_8bit(0x05)

    def set_gram_scan_way(self, scan_dir):
        """
        Set the display scan and color transfer modes
        :param scan_dir: Scan direction
        :return: None
        """
        # Get the screen scan direction
        self.LCD_Scan_Dir = scan_dir

        # Get GRAM and LCD width and height
        if (scan_dir == L2R_U2D) or (scan_dir == L2R_D2U) or (scan_dir == R2L_U2D) or (scan_dir == R2L_D2U):
            self.width = LCD_HEIGHT
            self.height = LCD_WIDTH
            if scan_dir == L2R_U2D:
                memory_access_reg_data = 0X00 | 0x00
            elif scan_dir == L2R_D2U:
                memory_access_reg_data = 0X00 | 0x80
            elif scan_dir == R2L_U2D:
                memory_access_reg_data = 0x40 | 0x00
            else:  # R2L_D2U:
                memory_access_reg_data = 0x40 | 0x80
        else:
            self.width = LCD_WIDTH
            self.height = LCD_HEIGHT
            if scan_dir == U2D_L2R:
                memory_access_reg_data = 0X00 | 0x00 | 0x20
            elif scan_dir == U2D_R2L:
                memory_access_reg_data = 0X00 | 0x40 | 0x20
            elif scan_dir == D2U_L2R:
                memory_access_reg_data = 0x80 | 0x00 | 0x20
            else:  # R2L_D2U
                memory_access_reg_data = 0x40 | 0x80 | 0x20

        # please set (memory_access_reg_data & 0x10) != 1
        if (memory_access_reg_data & 0x10) != 1:
            self.LCD_X_Adjust = LCD_Y
            self.LCD_Y_Adjust = LCD_X
        else:
            self.LCD_X_Adjust = LCD_X
            self.LCD_Y_Adjust = LCD_Y

        # Set the read / write scan direction of the frame memory
        self.write_register(0x36)  # MX, MY, RGB mode
        if LCD_1IN44 == 1:
            self.write_data_8bit(memory_access_reg_data | 0x08)  # 0x08 set RGB
        else:
            self.write_data_8bit(memory_access_reg_data & 0xf7)  # RGB color filter panel

    def init(self, lcd_scan_dir):
        """
        Initialization of the LCD
        :param lcd_scan_dir: Scan direction
        :return: -1 if initialization fails, 0 otherwise
        """
        if config.gpio_init() != 0:
            return -1

        # Turn on the backlight
        GPIO.output(config.LCD_BL_PIN, GPIO.HIGH)

        # Hardware reset
        self.reset()

        # Set the initialization register
        self.init_register()

        # Set the display scan and color transfer modes
        self.set_gram_scan_way(lcd_scan_dir)
        config.driver_delay_ms(200)

        # sleep out
        self.write_register(0x11)
        config.driver_delay_ms(120)

        # Turn on the LCD display
        self.write_register(0x29)

    def set_windows(self, x_start, y_start, x_end, y_end):
        """
        Sets the start position and size of the display area
        :param x_start: X direction Start coordinates
        :param y_start: Y direction Start coordinates
        :param x_end: X direction end coordinates
        :param y_end: Y direction end coordinates
        """
        # set the X coordinates
        self.write_register(0x2A)
        self.write_data_8bit(0x00)
        self.write_data_8bit((x_start & 0xff) + self.LCD_X_Adjust)
        self.write_data_8bit(0x00)
        self.write_data_8bit(((x_end - 1) & 0xff) + self.LCD_X_Adjust)

        # set the Y coordinates
        self.write_register(0x2B)
        self.write_data_8bit(0x00)
        self.write_data_8bit((y_start & 0xff) + self.LCD_Y_Adjust)
        self.write_data_8bit(0x00)
        self.write_data_8bit(((y_end - 1) & 0xff) + self.LCD_Y_Adjust)

        self.write_register(0x2C)

    def clear(self):
        """
        Clears the display
        :return: None
        """
        _buffer = [0xff] * (self.width * self.height * 2)
        self.set_windows(0, 0, self.width, self.height)
        GPIO.output(config.LCD_DC_PIN, GPIO.HIGH)
        for i in range(0, len(_buffer), 4096):
            config.spi_write_byte(_buffer[i:i + 4096])

    def show_image(self, image):
        """
        Draws the image to the screen
        :param image: the image to be drawn
        :return: None
        """
        if not image:
            return
        width, height = image.size
        if width != self.width or height != self.height:
            raise ValueError('Image must be same dimensions as display ({0}x{1}).'.format(self.width, self.height))
        img = np.asarray(image)
        pix = np.zeros((self.width, self.height, 2), dtype=np.uint8)
        pix[..., [0]] = np.add(np.bitwise_and(img[..., [0]], 0xF8), np.right_shift(img[..., [1]], 5))
        pix[..., [1]] = np.add(np.bitwise_and(np.left_shift(img[..., [1]], 3), 0xE0), np.right_shift(img[..., [2]], 3))
        pix = pix.flatten().tolist()
        self.set_windows(0, 0, self.width, self.height)
        GPIO.output(config.LCD_DC_PIN, GPIO.HIGH)
        # noinspection PyTypeChecker
        for i in range(0, len(pix), 4096):
            config.spi_write_byte(pix[i:i + 4096])
