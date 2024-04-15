import unittest

from archerdfu.bmp.gui_fonts import bin2bmp, bmp2bin, ASCII_SIZE


class TestGuiFont(unittest.TestCase):

    def test_bin2bmp(self):
        bin2bmp('../assets/fonts.bin', '../assets/fonts_bin2bmp.bmp', ASCII_SIZE)

    def test_bmp2bin(self):
        bmp2bin('../assets/fonts_bin2bmp.bmp', '../assets/fonts_bmp2bin.bin')



