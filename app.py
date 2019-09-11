import os
import json
import time
import yaml
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
import mmos

app = Flask(__name__)

# Load the app's configuration (API keys / api secret)
default_path = os.path.join(app.root_path, "config.yaml")
with open(os.environ.get("CONFIG_PATH", default_path), "r") as f:
    c = yaml.safe_load(f)
    for key in c.keys():
        app.config[key] = c[key]

# Load up our custom MMOS client
m = mmos.Client(**app.config)


def template(name, **context):
    return render_template(name, config=app.config, **context)


# Load static resources
@app.route("/img/<path:path>")
def send_img(path):
    return send_from_directory("img", path)


# Handle tasks
@app.route("/", methods=["GET", "POST"])
def index():
    thanks = False

    if request.method == "POST":
        sex = request.values.get("sex")
        task_created = int(request.values.get("task_created"))
        task_id = int(request.values.get("task_id"))
        thanks = True

        print(json.dumps(m.classify(sex, task_created, task_id)))

    t = m.create_task()
    created = int(time.time() * 1000)
    return template("guess.html", t=t["task"], created=created, thanks=thanks)


if __name__ == "__main__":
    app.run()
