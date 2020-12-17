from flask import Flask ,redirect, url_for, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/map")
def map():
    zooom = "11"
    return render_template("map.html", zoom = f"{zooom}")

@app.route("/sam.geojson")
def map_route():
    return render_template("sam.geojson")


if __name__ == "__main__":
    app.run()

