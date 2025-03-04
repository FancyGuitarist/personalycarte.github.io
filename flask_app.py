from flask import Flask, render_template, flash, request, redirect, url_for


app = Flask(__name__, template_folder='.')

time_keys = ["bus", "car", "bike", "walk"]


def init_times():
    times = {}
    for key in time_keys:
        times[key] = "00:00"
    return times


def get_times():
    times = {}
    for key in time_keys:
        times[key] = request.form.get(key)
    return times


app.secret_key = "your_secret_key"  # Required for flashing messages


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        times = get_times()

        # Flash the submitted values (visible on the web page)
        flash(f"Bus: {times['bus']}, Car: {times['car']}, Bike: {times['bike']}, Walk: {times['walk']}")

        return redirect(url_for("home"))  # Redirect to avoid form resubmission
    else:
        times = init_times()
    return render_template("index.html", times=times)  # Load the HTML form


@app.route("/submit_times", methods=["POST"])
def submit_times():
    times = get_times()

    # Flash the submitted values (visible on the web page)
    flash(f"Bus: {times['bus']}, Car: {times['car']}, Bike: {times['bike']}, Walk: {times['walk']}")

    return render_template("index.html", times=times)


if __name__ == "__main__":
    app.run(debug=True)
