from flask import Flask, render_template, flash, request, redirect, url_for


app = Flask(__name__, template_folder='.')

time_keys = ["bus", "car", "bike", "walk"]
toggle_keys = ["toggleCar", "toggleBus", "toggleBike", "toggleWalk"]


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


def init_toggles():
    toggles = {}
    for key in toggle_keys:
        if key == "toggleCar":
            toggles[key] = "on"
        else:
            toggles[key] = ""
    return toggles


def get_toggles():
    toggles = {}
    for key in toggle_keys:
        try:
            toggles[key] = request.form.get(key)
        except KeyError:
            toggles[key] = ""
    return toggles


app.secret_key = "your_secret_key"  # Required for flashing messages


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        times = get_times()
        toggle_states = get_toggles()

        # Flash the submitted values (visible on the web page)
        flash(f"Bus: {times['bus']}, Car: {times['car']}, Bike: {times['bike']}, Walk: {times['walk']}")
        flash(f"Selected modes: {toggle_states}")

        return redirect(url_for("home"))  # Redirect to avoid form resubmission
    else:
        times = init_times()
        toggle_states = init_toggles()
    return render_template("index.html", times=times, toggle_states=toggle_states)  # Load the HTML form


@app.route("/map")
def map_page():
    return render_template("carte_first.html")


@app.route("/submit_inputs", methods=["POST"])
def submit_inputs():
    times = get_times()
    toggle_states = get_toggles()
    print(times)
    print(toggle_states)

    # Flash the submitted values (visible on the web page)
    flash(f"Bus: {times['bus']}, Car: {times['car']}, Bike: {times['bike']}, Walk: {times['walk']}")
    # flash(f"Selected modes: {toggle_states}")

    return render_template("index.html", times=times, toggle_states=toggle_states)  # Load the HTML form


if __name__ == "__main__":
    app.run(debug=True)
