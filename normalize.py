### Utility script for normalizing katakana image data ###

# import

from PIL import Image
import os

# constants
katakana = ['a', 'i', 'u', 'e', 'o',
            'ka', 'ki', 'ku', 'ke', 'ko',
            'sa', 'shi', 'su', 'se', 'so',
            'ta', 'chi', 'tsu', 'te', 'to',
            'na', 'ni', 'nu', 'ne', 'no',
            'ha', 'hi', 'fu', 'he', 'ho',
            'ma', 'mi', 'mu', 'me', 'mo',
            'ya', 'yu', 'yo',
            'ra', 'ri', 'ru', 're', 'ro',
            'wa', 'wo', 'n']

# variables

base = "data\\"
dirs = ["computer (gray)\\", "natural (good)\\"]

# functions

def gray(img):
    """convert image to grayscale"""
    return trans(img.convert("RGBA")).convert("LA")

def trans(img):
    """turn transparent pixels into white pixels, assumes 'rgba' mode"""
    pxs = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if pxs[x, y][3] < 255:
                pxs[x, y] = (255, 255, 255, 255) #(255 - pxs[x, y][3] ,) * 3 + (255 ,)
    return img

def intensity(img):
    """scale intensity of image"""
    minpix = min([c[1][0] for c in img.getcolors()]) if img.getcolors() != None else 0
    maxpix = max([c[1][0] for c in img.getcolors()]) if img.getcolors() != None else 256
    pxs = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pxs[x, y] = ((pxs[x, y][0] - minpix) * 255 // (maxpix - minpix), 255)
    return img

def crop(img):
    """crop image so that background is removed, also white out background colors"""
    pxs = img.load()
    bg = max(img.getcolors())[1][0]
    top = left = 1000
    bot = right = 0
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            px = img.getpixel((x, y))[0]
            if (abs(bg - px) > 30):
                top = min(top, y)
                left = min(left, x)
                bot = max(bot, y)
                right = max(right, x)
            else:
                pxs[x, y] = (255, 255)
    diff = abs(right - left) - abs(bot - top)
    if (diff < 0):
        right = right + abs(diff) // 2
        left = left - abs(diff) // 2
    else:
        bot = bot + abs(diff) // 2
        top = top - abs(diff) // 2
    return img.crop((max(left - 1, 0), max(top - 1, 0), min(right + 1, img.size[0]), min(bot + 1, img.size[1])))

def binary(img):
    """converts image to black and white, TODO"""
    pass

def resize(img):
    """resize image to 16 x 16"""
    return img.resize((16, 16), Image.ANTIALIAS) if img.size[0] > 16 else img.resize((16, 16))

def normalize(img):
    """apply all normalizations, return normalized image"""
    return resize(intensity(crop(gray(img))))

def preprocess():
    """preprocess all images, apply normalization"""
    for d in dirs:
        for f in os.listdir(base + d):
            for k in katakana:
                img = Image.open(base + d + f + "\\" + k + ".png")
                nor = normalize(img)
                nor.save(base + d + f + "\\" + k + "_norm.png")

if __name__ == "__main__":
    preprocess()
