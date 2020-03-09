from app.tasks import create_image_set
from app import app
from app.tasks import count_words
from app import r
from app import q

from flask import render_template, request, redirect, url_for, flash

from time import strftime
import os
import secrets
app.config['SECRET_KEY'] = 'sfsfsecra24545sfac'
app.config['UPLOAD_DIR'] = '/Users/sheltong/Desktop/julian_webscrape/app/static/img/uploads'


@app.route('/')
def index():
    return "hello world"


@app.route('/add-task', methods=["GET", "POST"])
def add_task():
    jobs = q.jobs
    message = None

    if request.args:
        url = request.args.get('url')

        task = q.enqueue(count_words, url)

        jobs = q.jobs

        q.len = len(q)

        message = f"Task queued at {task.enqueued_at.strftime('%a %d %b %Y %H:%M:%S')}. {q.len} jobs queued"

    return render_template('add_task.html', message=message, jobs=jobs)


@app.route('/upload-image', methods=["GET", "POST"])
def upload_image():

    message = None

    if request.method == "POST":
        image = request.files["image"]
        image_dir_name = secrets.token_hex(16)
        os.mkdir(os.path.join(app.config["UPLOAD_DIR"], image_dir_name))

        image.save(os.path.join(
            app.config["UPLOAD_DIR"], image_dir_name, image.filename))
        image_dir = os.path.join(
            app.config["UPLOAD_DIR"], image_dir_name)
        q.enqueue(create_image_set, image_dir, image.filename)
        flash("Image uploaded and sent for resizing", "success")
        message = f"/image/{image_dir_name}/{image.filename.split('.')[0]}"

    return render_template('upload_image.html', message=message)


@app.route("/image/<dir>/<img>")
def view_image(dir, img):
    return render_template("view_image.html", dir=dir, img=img)
