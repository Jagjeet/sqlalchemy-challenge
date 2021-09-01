# sqlalchemy-challenge

This project explores hawaii climate data in two parts:

* The first is a Jupyter notebook that explores precipitation, temperature and station data from a sqllite database using SQLAlchemy
* The second takes the queries developed in the first part and modifies them slightly to develop an API run from `flask`

Note: The bonus for this challenge was not completed.

## Prerequisites

To run this project the folowing tools are needed:

* Jupyter Notebooks and/or Jupyter Labs (for CSV data exploration)
* Anaconda is recommended though library dependencies can be installed individually as well
* Flask

## Usage

* Clone the respository
* Run the notebook `climate.ipynb` for preliminary precipitation and station analysis.
* Run `flask run` to run the API which can be found in `app.py`
  * Navigate to `http://127.0.0.1:5000/` or the URL where you flask app is running for a description of the API routes.


## Known Issues

* Code is not production ready
* No parameter checking is implemented
* No error checking is implemented
* Minimal edge testing was completed

## References

* [Flask Development Mode](https://stackoverflow.com/questions/52162882/set-flask-environment-to-development-mode-as-default)
* [Escape Tags in HTML](https://stackoverflow.com/questions/692123/escape-tags-in-html)
