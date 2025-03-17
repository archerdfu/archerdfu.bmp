from itertools import batched

from PIL import Image

TRASHOLD = 127
GLYPH_SIZE = 16


def encode_glyphs(*imgs):
    buffer = bytearray()
    gw, gh = GLYPH_SIZE, GLYPH_SIZE * 2
    for img in imgs:
        img = img.convert('L')
        w, h = img.size
        if w != gw or h % gw:
            raise Exception('Image width must be 16 pixels and height a quant of 16 pixels')
        px = img.load()
        for y in range(h):
            line = bytearray()
            for x in range(w):
                line += b'\xc0' if px[x, y] > TRASHOLD else b'\x00'
            buffer += line * 2  # double icon line
            if y % gw == 0:  # mark icon start
                buffer[y * gh] += 1
    return buffer


def decode_glyphs(*glyphs: [bytes, bytearray]) -> Image.Image:
    buffer = b''.join(glyphs)
    gw, gh = GLYPH_SIZE, GLYPH_SIZE * 2
    count = len(buffer) // (gw * gh)
    if count < 1:
        raise Exception('glyphs count must be at least 1')

    img = Image.new("L", (gw, count * gw))
    px = img.load()

    x, y = 0, 0
    icons = batched(buffer, gw * gh)
    for ic in icons:
        lines = [line[:gw] for line in batched(ic, gh)]
        for l in lines:
            for b in l:
                px[x, y] = 255 if b > TRASHOLD else 0
                x += 1
            x = 0
            y += 1
    return img


if __name__ == '__main__':
    with open(r"assets/05-#14-ASCII_CYRILLIC--cyrillic_ukraine.dfu", 'rb') as fp:
        d = fp.read()[4096:]
        im = decode_glyphs(d)
        im.save("assets/cyrillic.bmp")
        gl = encode_glyphs(im)
        assert gl == d

    with open(r"assets/06-#13-ASCII_LATIN--latin_v7.dfu", 'rb') as fp:
        d = fp.read()[4096:]
        im = decode_glyphs(d)
        im.save("assets/latin.bmp")
        gl = encode_glyphs(im)
        # assert gl == d
        for i, j in enumerate(d):
            if gl[i] != j:
                print(i, i // (32 * 16), gl[i], j)
