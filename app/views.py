from app import app
from app.tasks import count_words
from app import r
from app import q

from flask import render_template, request

from time import strftime


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
