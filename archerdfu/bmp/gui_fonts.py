import os

from archerdfu.bmp.processing import matrix_to_bmp, bmp_to_matrix

PICTOGRAM_SIZE = 32
ASCII_SIZE = 16

__all__ = ['ASCII_SIZE', 'PICTOGRAM_SIZE', 'bytes_to_bmp', 'bmp_to_bytes']


# def bytes_to_bmp(in_buf: bytes, font_size: int) -> bytes:
#     images = parse_binary(in_buf, font_size)
#     out_buf = concatenate_images_vertically(images)
#     return out_buf
#
#
# def bmp_to_bytes(in_buf: bytes, font_size: int) -> bytes:
#     images = parse_concatenated_bmp(in_buf, font_size)
#     out_buf = build_binary(images, font_size)
#     return out_buf


# def make_bmp(buf, size):
#     arr = bytearray(buf)
#     length = size
#
#     img = Image.new('RGB', (size, size))
#     buf_list = [arr[i:i + length] for i in range(0, len(arr), length) if (i // length) % 2 == 0]
#     for r, row in enumerate(buf_list):
#         for c, col in enumerate(row):
#             if col <= 1:
#                 img.putpixel((c, r), (255, 255, 255))
#     return img


def split_list(input_list, chunk_size):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]


def convert_8bit_to_hex_rgb(color_value):
    # Ensure color value is within range
    color_value = max(0, min(255, color_value))
    # Convert 8-bit grayscale to 24-bit RGB
    # hex_rgb = '{:02x}{:02x}{:02x}'.format(color_value, color_value, color_value)
    # return '#' + hex_rgb
    # Convert 8-bit grayscale to 24-bit RGB integer
    rgb_int = (color_value << 16) + (color_value << 8) + color_value
    return rgb_int


def bin2bmp(input: [str, os.PathLike], output: [str, os.PathLike], font_size: int = ASCII_SIZE) -> None:
    mapping = {
        0: 0xFFFFFF,

    }

    with open(input, 'rb') as fp:
        in_buf = fp.read()

    matrix = []
    icons_buf = split_list(in_buf, font_size ** 2 * 2)

    for icon_buf in icons_buf:
        icon_rows_buf = split_list(icon_buf, font_size)[::2]  # removes each unpair row
        # _matrix = [
        #     [0xFFFFFF if i == 0 else 0xFF0000 if i == 1 else 0 for i in row_buf]
        #     for row_buf in icon_rows_buf
        # ]

        _matrix = [
            # [(~i & 0xFF) - 0x0000FF for i in row_buf]
            [convert_8bit_to_hex_rgb(~i & 0xFF) for i in row_buf]
            for row_buf in icon_rows_buf
        ]

        matrix.extend(_matrix)

    matrix.reverse()  # TODO: fix it in processor
    matrix_to_bmp(matrix, output, 24)


def bmp2bin(input: [str, os.PathLike], output: [str, os.PathLike]) -> None:
    matrix = bmp_to_matrix(input)
    matrix.reverse()  # TODO: fix it in processor
    buffer = b''
    for row in matrix:
        row_buf = bytearray([~(i >> 16) & 0xFF for i in row])

        buffer += row_buf
        row_buf_0 = row_buf[0]
        row_buf[0] = row_buf_0 - 0x01 if row_buf_0 in (0xc1, 0x01) else row_buf_0
        buffer += row_buf

    with open(output, 'wb') as fp:
        fp.write(buffer)

# def parse_binary(buf: bytes, size):
#     images = []
#     arr = bytearray(buf)
#     length = size * size * 2
#     buf_list = [arr[i:i + length] for i in range(0, len(arr), length)]
#     for f, bin in enumerate(buf_list):
#         images.append(make_bmp(bin, size))
#     return images
#
#
# def concatenate_images_vertically(images: list[Image]):
#     # Determine the dimensions of the concatenated profiles_image
#     image_width = images[0].width  # Assuming all images have the same width
#     size = sum(image.height for image in images)
#
#     # Create a new blank profiles_image with the calculated dimensions
#     concatenated_image = Image.new('RGB', (image_width, size))
#
#     # Concatenate the images vertically by pasting them onto the blank profiles_image
#     y_offset = 0
#
#     draw = ImageDraw.Draw(concatenated_image)
#
#     for image in images:
#
#         concatenated_image.paste(image, (0, y_offset))
#         y_offset += image.height
#
#         draw.line(((0, y_offset), (image_width, y_offset)), width=1, fill=0x0000FF)
#         y_offset += 1
#
#
#     # Save the concatenated profiles_image as a new BMP file
#     # concatenated_image.save(output_path, "BMP")
#     bytes_io = io.BytesIO()
#     concatenated_image.save(bytes_io, format='BMP')
#     bytes_io.seek(0)
#     return bytes_io.getvalue()
#
#
# def parse_concatenated_bmp(buf: bytes, size: int) -> list[Image]:
#     # Open the concatenated BMP file
#     bytes_io = io.BytesIO(buf)
#     concatenated_image = Image.open(bytes_io)
#
#     # Determine the number of images in the concatenated file
#     num_images = concatenated_image.height // size
#
#     # Split the concatenated profiles_image into individual images
#     images = []
#     y_offset = 0
#     for _ in range(num_images):
#         image = concatenated_image.crop((0, y_offset, concatenated_image.width, y_offset + size))
#         images.append(image)
#         y_offset += size + 1
#
#     return images
#
#
# def build_binary(imgs: list[Image], size):
#     output = b''
#     for img in imgs:
#         width, height = img.size
#         if width != height != size:
#             raise ValueError('Wrong .bmp font_size, must be 32x32px')
#
#         pixel_array = b''
#
#         for y in range(height):
#             row = b''
#             for x in range(width):
#                 r, g, b = img.getpixel((x, y))
#                 row += b'\x00' if r == g == b == 255 else b'\xC0'
#             pixel_array += row * 2
#             if pixel_array[0] <= 1:
#                 pixel_array = b'\x01' + pixel_array[1:]
#             else:
#                 pixel_array = b'\xC1' + pixel_array[1:]
#
#         output += pixel_array
#     return output
