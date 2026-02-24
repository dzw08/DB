"""Reads DesignBuilder EnergyPlus Output files."""

# libraries
# import matplotlib as mpl
from json import dump

from db_eplusout_reader import Variable, get_results
from db_eplusout_reader.constants import H

# parse output file, usually ask for user input, however using example for now

# print("Enter eso file path")
# path = input()
PATH_TO_FILE = r"/home/dani/DB/eplusout.sql"


def collect_temperature_results(path):
    """Using db_eplusout_reader to extract temperature results from eplusout SQL file.

    Parameters
    ----------
    path : location of sql file to be parsed

    Returns
    -------
    dictionary
        Results of file parsing.
    """
    return get_results(path, variables=[Variable(None, None, "C")], frequency=H)


# collecting temperature results
temperature_results = collect_temperature_results(PATH_TO_FILE)

# casting to list so can be serialized to json object, just using values
temperature_results_values = list(temperature_results.values())
with open("results_values.json", "w") as f:
    dump(temperature_results_values, f, indent=4)

# casting to list so can be serialied to json objects, just using headers/keys
temperature_results_keys = list(temperature_results.keys())
with open("results_keys.json", "w") as f:
    dump(temperature_results_keys, f, indent=4)

# plot the results using matplotlib
