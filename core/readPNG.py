import os.path
from tkinter import PhotoImage
from typing import List, Tuple
import zlib

def readFile():
    # with open('../map.png', 'rb') as f:
    #     return f.read()
    current_dir = os.path.dirname(__file__)
    map_path = os.path.abspath(os.path.join(current_dir, '..', 'map.png'))
    try:
        with open(map_path, 'rb') as f:
            return f.read()
    except:
        return None

def extractIDATchunks(png_bytes: bytes) -> bytes:
    pos = 8
    idat_data = bytearray()

    while pos < len(png_bytes):
        chunk_length = int.from_bytes(png_bytes[pos:pos+4], "big")
        chunk_type = png_bytes[pos+4:pos+8]
        chunk_data = png_bytes[pos+8:pos+8+chunk_length]
        chunk_crc = png_bytes[pos+8+chunk_length:pos+12+chunk_length]

        if chunk_type == b'IDAT':
            idat_data.extend(chunk_data)
        pos += 12 + chunk_length
    return bytes(idat_data)

def parseIHDR(png_bytes: bytes) -> (int, int):
    pos=8

    while pos < len(png_bytes):
        length = int.from_bytes(png_bytes[pos:pos+4], "big")
        chunk_type = png_bytes[pos+4:pos+8]
        if chunk_type == b'IHDR':
            width = int.from_bytes(png_bytes[pos+8:pos+12], "big")
            height = int.from_bytes(png_bytes[pos+12:pos+16], "big")
            return width, height
        pos += 8 + length + 4
    raise ValueError("IHDR chunk not found")


def decompressData(data: bytes) -> bytes:
    return zlib.decompress(data)


def decodeIDAT() -> list:
    png_bytes = readFile()
    width, height = parseIHDR(png_bytes)
    idat_data = extractIDATchunks(png_bytes)
    decompressed = decompressData(idat_data)

    image = decodePixels(decompressed, width, height)

    return image




def decodePixels(raw_data: bytes, width: int, height: int) -> (int, int, int):
    bytes_per_pixel = 3 #R, G, B
    stride = width * bytes_per_pixel
    offset = 0
    pixels: List[List[int]] = []

    for row in range(height):
        filter_type = raw_data[offset]
        offset += 1

        if filter_type != 0:
            raise NotImplementedError(f"Filter type: {filter_type} not supported in reading PNG files")

        row_data = raw_data[offset:offset+stride]
        offset += stride

        row_pixels = []

        for i in range(0, stride, 3):
            r = row_data[i]
            g = row_data[i+1]
            b = row_data[i+2]

            row_pixels.append((r, g, b))

        pixels.append(row_pixels)
    return pixels

def rgb_to_hex(rgb):
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

def pixels_to_tkinter_photoimage(pixels):
    height = len(pixels)
    width = len(pixels[0])

    img = PhotoImage(width=width, height=height)

    for y in range(height):
        row = " ".join(rgb_to_hex(p) for p in pixels[y])
        img.put("{" + row + "}", to=(0, y))

    return img