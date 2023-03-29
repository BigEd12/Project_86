from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

from pixels import PixelCounter


#---------------------- FLASK ----------------------#
app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def user_input():
    #Check if the POST request has the file part
    if 'fileInput' not in request.files:
        return 'No file uploaded'

    file = request.files['fileInput']

    #If the user does not select a file, the browser submits an empty file
    if file.filename == '':
        return 'No file selected'

    #Save the uploaded file to disk
    filename = secure_filename(file.filename)
    file_path = 'static/images/' + filename
    file.save(file_path)

    #Gets number of colours from user input
    num_colours = int(request.form.get('numColors'))

    #Creates a PixelCounter object to count the colours in the image
    counter = PixelCounter(file_path)
    rgb_codes = counter.count_pixels()

    #Check RGB codes and remove similar colours
    rgb_filtered = counter.remove_similar_colours(rgb_codes)

    #Returns user requested number of most frequently used colours
    top_rgb_codes = rgb_filtered[:num_colours]

    return render_template("index.html", image_path=filename, top_colours=top_rgb_codes)


if __name__ == "__main__":
    app.run(debug=True)