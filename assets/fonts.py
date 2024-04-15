from archerdfu.apis.typedefs.segments.bitmap2dfu import *
from archerdfu.bmp import bmp_to_matrix

if __name__ == '__main__':

    with open('fonts.bin', 'rb') as fp:
        buf = fp.read()
    bmp = bytes_to_bmp(buf, ASCII_SIZE)

    with open('newfonts.bin', 'wb') as fp:
        print(buf)
        buf = bmp_to_bytes(bmp, ASCII_SIZE)
        fp.write(buf)

        with open('fonts_back.bmp', 'wb') as fp:
            bmp = bytes_to_bmp(buf, ASCII_SIZE)
            fp.write(bmp)
        # bmp = bytes_to_bmp(buf, ASCII_SIZE)

