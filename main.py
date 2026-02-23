"""Reads DesignBuilder EnergyPlus Output files."""

# libraries
# import matplotlib as mpl
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


temperature_results = collect_temperature_results(PATH_TO_FILE)
print(temperature_results)
