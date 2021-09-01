from flask import Flask, jsonify
FLASK_DEBUG = 1

# Dictionary of Justice League
dummy_json = [
    {"blah": "blahblah", "blahblahblah": "blahblahblahblah"},
]

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(dummy_json)

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(dummy_json)

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(dummy_json)

@app.route("/api/v1.0/<start>")
def start_period(start):
    return calc_period(start, '2017-08-23')

@app.route("/api/v1.0/<start>/<end>")
def full_period(start, end):
    return calc_period(start, end)

def calc_period(start, end):
    return jsonify(dummy_json)

@app.route("/")
def welcome():
    return (
        f"<html>"
        f"<head>"
        f"<title>Climate API</title>"
        f"</head>"
        f"<body>"
        f"<h1>Welcome to the Climate API!</h1>"
        f"<h2>Available Routes:</h2>"
        f"<ul>"
        f"<li><a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a></li>"
        f"<li><a href='/api/v1.0/stations'>/api/v1.0/stations</a></li>"
        f"<li><a href='/api/v1.0/tobs'>/api/v1.0/tobs</a></li>"
        f"<li>/api/v1.0/&#60;start&#62;"
        f"<ul><li>e.g. <a href='/api/v1.0/2015-08-20'>/api/v1.0/2015-08-20</a></li></ul></li>"
        f"<li>/api/v1.0/&#60;start&#62;/&#60;end&#62;</li>"
        f"<ul><li>e.g. <a href='/api/v1.0/2015-08-20/2017-08-23'>/api/v1.0/2015-08-20/2017-08-23</a></li></ul></li>"
        f"<li>Note: &#60;start&#62; and &#60;end&#62; refer to dates starting from 2010-01-01 to 2017-08-23</li>"
        f"<li>Dates should be formatted as YYYY-MM-DD format</li>"
        f"</ul>"
        f"</body>"
        f"</html>"
    )


if __name__ == "__main__":
    app.run(debug=True)
