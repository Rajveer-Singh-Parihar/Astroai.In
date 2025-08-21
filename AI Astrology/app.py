from flask import Flask, render_template, request
from static.prediction import build_profile

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    profile = None
    if request.method == "POST":
        name = request.form.get("name")
        dob = request.form.get("dob")
        if name and dob:
            profile = build_profile(name, dob)
    return render_template("index.html", profile=profile)

if __name__ == "__main__":
    app.config["ENV"] = "production"
    app.config["DEBUG"] = False
    app.run(debug=False, use_reloader=False)
