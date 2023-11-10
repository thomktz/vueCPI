import os
import logging
import pytz

from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS

from cpilib import HICP 
from cpilib.constants import EA19
from cpilib.utils import coicop_labels

def last_update_date(path):
    """Get the last update time of a file."""
    timestamp = os.path.getmtime(path)
    last_modified_date = datetime.fromtimestamp(timestamp, pytz.utc)
    paris_timezone = pytz.timezone('Europe/Paris')
    paris_date = last_modified_date.astimezone(paris_timezone)
    print("Time:", paris_date.strftime("%Y-%m-%d %H:%M:%S"), flush=True)
    return paris_date.strftime("%Y-%m-%d %H:%M:%S")

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

# Load HICP data with 1 day cache limit
hicp = HICP.from_cache(time_limit=1)

# Transform the dictionary into a list of dicts
countries = (
    [{"value": "EA19", "label": "Euro Area"}] 
    + [{"value": k, "label": v} for k, v in EA19.items()]
)

# Create the COICOP hierarchy
nodes = {}
for _, row in coicop_labels.iterrows():
    code = row["code"]
    label = row["label"]
    nodes[code] = {"label": label, "children": []}
for code in nodes:
    if code == "00":
        continue
    parent_code = code[:-1] if len(code) > 2 else "00"
    nodes[parent_code]["children"].append(code)


# Create routes
@app.route("/countries", methods=["GET"])
def get_countries():
    """Dictionary of country codes and labels."""
    return jsonify(countries)

@app.route("/node/<code>")
def get_node(code):
    """Get information on a particular node (label, children codes)."""
    node = nodes.get(code)
    if node is None:
        return jsonify({"error": "Node not found"}), 404
    return jsonify(node)

@app.route("/data/<country>/<code>")
def get_data(country, code):
    """Get data for a particular node."""
    if country=="all":
        return jsonify({"error": "Not implemented yet"}), 404
    if country=="GR":
        country = "EL"
    try:
        values = hicp.prices.node("CP"+code, country).dropna()
    except:
        return jsonify({"error": "Error when fetching data"}), 404
    
    as_df = values.reset_index()
    as_df.columns = ["date", "value"]
    as_df["date"] = as_df["date"].dt.strftime("%Y-%m-%d")
    data = as_df.to_dict("records")
    return jsonify(data)

@app.route("/weights/<country>/<code>")
def get_weights(country, code):
    """Get weights for a particular node."""
    if country=="all":
        return jsonify({"error": "Not implemented yet"}), 404
    if country=="GR":
        country = "EL"
    try:
        country_w = hicp.country_weights[country].iloc[-1]
        item_w = hicp.weights.node("CP" + code, country).iloc[-1]
    except:
        return jsonify({"error": "Error when fetching data"}), 404

    return jsonify({"country": country_w, "item": item_w})

@app.route("/last-update")
def last_update():
    """Get the last update time of the data."""
    try:
        return jsonify({"last_update": last_update_date("cache/prices.parquet")})
    except OSError:
        return jsonify({"error": "Data file not found"}), 404

@app.route("/refresh", methods=["GET"])
def refresh_data():
    global hicp
    # Refresh the data
    hicp = HICP.from_cache(time_limit=0)

    return jsonify({"message": "Data refreshed", "last_refresh_time": last_update_date("cache/prices.parquet")}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)