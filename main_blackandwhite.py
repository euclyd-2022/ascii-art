from PIL import Image, ImageDraw, ImageFont
from math import floor


chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

charList = list(chars)
charLen = len(charList)
interval = charLen/256

def getChar(inputInt):
    return charList[floor(inputInt*interval)]



with Image.open("download.jpg") as im:
    #greyscale convert
    im = im.convert("L")


    width = im.size[0]
    height = im.size[1]
    px = im.load()

    print(width, height)
    text_file = open("output.txt", "w")
    outputImage = Image.new("L", (width, height), color=0)
    d = ImageDraw.Draw(outputImage)
    font = ImageFont.truetype("./cour.ttf", 18)
    for y in range(0, height, 18):
       for x in range(0, width, 18):
            xy =(x,y)

            value = im.getpixel(xy)
            text_file.write(getChar(value))
            getChar(value)
            d.text(xy, getChar(value), font=font, fill=255, spacing=10)
       text_file.write("\n")



    outputImage.save("output.jpg")






