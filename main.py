import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '../'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

OUTPUT_FOLDER = os.path.join('static', 'output')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

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

    return render_template("uploaded.html")


if __name__ == "__main__":
    app.run(debug=True)
