from flask import Flask, render_template, request
from static.prediction import build_profile

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    profile = None
    error = None
    if request.method == "POST":
        name = request.form.get("name")
        dob = request.form.get("dob")
        if name and dob:
            try:
                profile = build_profile(name, dob)
                print(f"Profile created successfully: {profile['name']}, {profile['zodiac']}, {profile['life_path']}")
            except ValueError as e:
                # Handle date parsing errors specifically
                error = str(e)
                print(f"Date parsing error: {e}")
            except Exception as e:
                error = f"Error processing your data: {str(e)}"
                print(f"Unexpected error: {e}")
        else:
            error = "Please provide both name and date of birth"
    return render_template("index.html", profile=profile, error=error)

if __name__ == "__main__":
    app.config["ENV"] = "development"
    app.config["DEBUG"] = True
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
