import time
from flask import Flask, render_template, url_for, request, redirect, flash
from PIL import Image, ImageDraw, ImageFont
from math import floor
from werkzeug.utils import secure_filename
from os.path import exists
from os import remove, stat

UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "notasecret"

def allowed_file(filename):
    #returns bool
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


file_exists = False
@app.route("/", methods=["POST", "GET"])
def home():
    chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    # def get_file_or_folder_age(path):
    #
    #     # getting ctime of the file/folder
    #     # time will be in seconds
    #     if exists(path):
    #         ctime = stat(path).st_ctime
    #     else:
    #         ctime = 0
    #
    #     # returning the time
    #     return ctime

    def make_image(file):
        global file_exists
        charList = list(chars)
        charLen = len(charList)
        interval = charLen/256

        def getChar(inputInt):
            return charList[floor(inputInt*interval)]

        with Image.open(file) as im:
            width = im.size[0]
            height = im.size[1]
            px = im.load()

            print(width, height)

            outputImage = Image.new("RGB", (width, height), color=(200,200,200))
            d = ImageDraw.Draw(outputImage)
            font = ImageFont.truetype("./cour.ttf", 18)
            for y in range(0, height, 18):
               for x in range(0, width, 18):
                    xy =(x,y)
                    r, g, b = px[xy]
                    value = int(r/3 + g/3 + b/3)

                    getChar(value)
                    d.text(xy, getChar(value), font=font, fill=(r, g, b), spacing=10)




            outputImage.save(f"{UPLOAD_FOLDER}output_colour.jpg")
            remove(f"{UPLOAD_FOLDER}{filename}")
            print(f"{UPLOAD_FOLDER}{filename} removed")


    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{UPLOAD_FOLDER}{filename}")
            # run ascii function
            make_image(f"{UPLOAD_FOLDER}{filename}")
            return redirect(url_for('home'))
        else:
            flash("error with upload")

    path = f"{UPLOAD_FOLDER}output_colour.jpg"
    # if exists(path) and get_file_or_folder_age(path) < time.time()+1000:
    #     remove(path)


    if exists(path):
        file_exists = True
    else:
        file_exists = False
    return render_template("index.html", file_exists=file_exists)




if __name__ == '__main__':
    app.run(debug=True)
