from flask import Flask, render_template, flash, request, redirect, url_for
from itinerary import CustomItinerary
import time  # For testing purposes

app = Flask(__name__, template_folder=".")

time_keys = ["bus", "car", "bike", "walk"]
toggle_keys = ["toggleCar", "toggleBus", "toggleBike", "toggleWalk"]
coordinates_keys = ["coords_origin", "coords_destination"]


def init_times():
    """
    Initialize the times dictionary with default values.
    :return:
    """
    times = {}
    for key in time_keys:
        times[key] = "00:00"
    return times


def get_times():
    """
    Get the times from the html form.
    :return:
    """
    times = {}
    for key in time_keys:
        times[key] = request.form.get(key)
    return times


def init_toggles():
    """
    Initialize the transport toggles dictionary with default values.
    Car is the only selected transport by default.
    :return:
    """
    toggles = {}
    for key in toggle_keys:
        if key == "toggleCar":
            toggles[key] = "on"
        else:
            toggles[key] = ""
    return toggles


def get_toggles_dict():
    """
    Get the transport toggles from the html form.
    :return:
    """
    toggles = {}
    for key in toggle_keys:
        try:
            toggles[key] = request.form.get(key)
        except KeyError:
            toggles[key] = ""
    return toggles


def convert_toggles_dict_to_list(toggles_dict):
    toggles = []
    for key in toggle_keys:
        if toggles_dict[key] == "on":
            toggles.append(key)
    return toggles


def get_coordinates_dict():
    """
    Get the coordinates from the html form.
    :return:
    """
    coordinates = {}
    for key in coordinates_keys:
        try:
            coordinates[key] = request.form.get(key)
        except KeyError:
            coordinates[key] = ""
    return coordinates


def convert_coordinates_dict_to_tuple(coordinates_dict):
    for key in coordinates_keys:
        coordinates_dict[key] = tuple(map(float, coordinates_dict[key].split(',')))
    return coordinates_dict


app.secret_key = "your_secret_key"  # Required for flashing messages


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        times = get_times()
        toggle_states = get_toggles_dict()

        # Flash the submitted values (visible on the web page)
        flash(
            f"Bus: {times['bus']}, Car: {times['car']}, Bike: {times['bike']}, Walk: {times['walk']}"
        )
        flash(f"Selected modes: {toggle_states}")

        return redirect(url_for("home"))  # Redirect to avoid form resubmission
    else:
        times = init_times()
        toggle_states = init_toggles()
    return render_template(
        "index.html", times=times, toggle_states=toggle_states
    )  # Load the HTML form


@app.route("/map")
def map_page():
    return render_template("carte_first.html")


@app.route("/submit_inputs", methods=["POST"])
def submit_inputs():
    times = get_times()
    toggle_states = get_toggles_dict()
    transport_modes = convert_toggles_dict_to_list(toggle_states)
    coordinates = convert_coordinates_dict_to_tuple(get_coordinates_dict())
    print(times)
    print(transport_modes)
    print(coordinates)
    itinerary = CustomItinerary()
    start_time = time.time()
    best_itinerary = itinerary.compute_itinerary(
        coordinates['coordinates_origin'],
        coordinates['coordinates_destination'],
        transport_modes)

    print(best_itinerary)
    print(f"Time to compute: {time.time() - start_time} seconds")

    # Flash the submitted values (visible on the web page)
    flash(
        f"Bus: {times['bus']}, Car: {times['car']}, Bike: {times['bike']}, Walk: {times['walk']}"
    )
    flash(f"Selected modes: {toggle_states}")

    return render_template(
        "index.html", times=times, toggle_states=toggle_states
    )  # Load the HTML form


if __name__ == "__main__":
    app.run(debug=True)
