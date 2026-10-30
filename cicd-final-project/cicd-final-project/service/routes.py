"""Counter routes."""
from flask import jsonify
from service import app

COUNTERS = {}


@app.route("/")
def index():
    """Health/info endpoint."""
    return jsonify(name="Counter Service", status="running"), 200


@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """Create a counter."""
    app.logger.info("Request to create counter: %s", name)
    if name in COUNTERS:
        return jsonify(error=f"Counter {name} already exists"), 409
    COUNTERS[name] = 0
    return jsonify(name=name, counter=0), 201


@app.route("/counters/<name>", methods=["GET"])
def read_counter(name):
    """Read a counter."""
    app.logger.info("Request to read counter: %s", name)
    if name not in COUNTERS:
        return jsonify(error=f"Counter {name} does not exist"), 404
    return jsonify(name=name, counter=COUNTERS[name]), 200


@app.route("/counters/<name>", methods=["PUT"])
def update_counter(name):
    """Increment a counter."""
    app.logger.info("Request to increment counter: %s", name)
    if name not in COUNTERS:
        return jsonify(error=f"Counter {name} does not exist"), 404
    COUNTERS[name] += 1
    return jsonify(name=name, counter=COUNTERS[name]), 200


@app.route("/counters/<name>", methods=["DELETE"])
def delete_counter(name):
    """Delete a counter."""
    app.logger.info("Request to delete counter: %s", name)
    if name not in COUNTERS:
        return jsonify(error=f"Counter {name} does not exist"), 404
    del COUNTERS[name]
    return "", 204
