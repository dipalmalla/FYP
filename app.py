import os

from flask import Flask, request,make_response, render_template, send_from_directory
from functools import wraps, update_wrapper
from datetime import datetime


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static/output/')

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        filename = file.filename

        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".jpeg"):
            destination = "/".join([target, filename])
            file.save(destination)

    print(os.stat(filename).st_size)

    from generate_map import HeatMap
    HeatMap.generate_map(filename)

    from combine_images import make_quality_compression
    from PIL import Image

    try:
        map = Image.open("static/output/msroi_map.jpg")
        image = Image.open(request.files['file'].stream)
        make_quality_compression(image, map)
    except IOError:
        pass

    return render_template("uploaded.html", original_image=filename)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("static/output", filename)


@app.route('/nocache')
def something_not_cached():
    resp = make_response(render_template("uploaded.html"))
    resp.cache_control.no_cache = True
    return resp


if __name__ == "__main__":
    app.run(debug=True)