from typing import Tuple
import numpy as np
from typing import List
import zlib
import struct
from typing import BinaryIO

Pixel = Tuple[int, int, int]

HEADER = b'\x89PNG\r\n\x1A\n'

#image = []

def initImage(width, height):
    return np.zeros((width, height, 3), dtype=np.uint8)

def getChecksum(chunk_type: bytes, data: bytes) -> int:
    checksum = zlib.crc32(chunk_type)
    checksum = zlib.crc32(data, checksum)
    return checksum

def chunk(out: BinaryIO, chunk_type: bytes, data: bytes) -> None:
    out.write(struct.pack('>I', len(data)))
    out.write(chunk_type)
    out.write(data)

    checksum = getChecksum(chunk_type, data)
    out.write(struct.pack('>I', checksum))

def encodeData(img) -> List[int]:
    ret = []

    for row in img:
        ret.append(0)

        color_values = [
            color_value
            for pixel in row
            for color_value in pixel

        ]
        ret.extend(color_values)
    return ret

def compressData(data: List[int]) -> bytes:
    data_bytes = bytearray(data)
    return zlib.compress(data_bytes)

def make_idat(img) -> bytes:
    encoded_data = encodeData(img)
    compressed_data = compressData(encoded_data)
    return compressed_data

def make_ihdr(width: int, height: int, bit_depth: int, color_type: int) -> bytes:
    return struct.pack('>2I5B', width, height, bit_depth, color_type, 0, 0, 0)

def dumpPNG(out: BinaryIO, img) -> None:
    out.write(HEADER)

    assert len(img) > 0
    width = len(img[0])
    height = len(img)
    bit_depth = 8
    color_type = 2

    ihdr_data = make_ihdr(width, height, bit_depth, color_type)
    chunk(out, b'IHDR', ihdr_data)

    compressed_data = make_idat(img)
    chunk(out, b'IDAT', data=compressed_data)

    chunk(out, b'IEND', data=b'')

def savePNG(img, filename: str) -> None:
    with open(filename, 'wb') as out:
        dumpPNG(out, img)

def setPixel(image, pixel: Pixel, x: int, y: int) -> None:
    image[y][x] = pixel


