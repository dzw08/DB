"""Reads DesignBuilder EnergyPlus Output files."""

# libraries
import matplotlib.pyplot as plt
from db_eplusout_reader import Variable, get_results
from db_eplusout_reader.constants import RP, TS, A, D, H, M
from numpy import arange


def collect_temperature_results(path: str, freq: str):
    """Using db_eplusout_reader to extract temperature results from eplusout SQL file.

    Parameters
    ----------
    path
        location of sql file to be parsed
    freq
        frequency of the data collection: "RP", "TS", "A", "D", "H", "M"

    Returns
    -------
    freq
        str
        frequency of the data collection: "RP", "TS", "A", "D", "H", "M"
    temp_results_keys
        list
        Location, description and units of temperatures.
    temp_results_values
        list
        Raw values of temperatures.
    """

    path = repr(path)[1:-1].strip()

    frequencies = {"TS": TS, "H": H, "D": D, "M": M, "A": A, "RP": RP}
    temp_results = get_results(
        path, variables=[Variable(None, None, "C")], frequency=frequencies[freq]
    )

    # retrieving actual temp values as well as locations
    temp_results_values = list(temp_results.values())
    temp_results_keys = list(temp_results.keys())

    return freq, temp_results_keys, temp_results_values


def plot_results(results_values: list, results_keys: list, data_type: str, freq: str):
    """Plots db-eplusout-reader output files in a line graph using matplotlib.

    Parameters
    ----------
    results_values
        LIST The actual values of the data.
    results_keys
        LIST What the values of the data refer to as well as their units.
    data_type
        STR What kind of data, e.g. Temperature or energy
    freq
        STR Frequency of data collection intervals

    Returns
    -------
    Plotted matplotlib data
    """

    units_passed = len(results_values[0])
    time_units = list(range(units_passed))

    plt.figure(dpi=100)
    for i, keys in enumerate(results_keys):
        plt.plot(
            time_units,
            results_values[i],
            label=f"{keys[0]} {keys[1]}",
        )

    # labels
    if freq == "TS":
        step = 1
        unit = "Time steps"
    if freq == "H":
        step = 24
        unit = "Days"
    if freq == "D":
        step = 1
        unit = "Days"
    if freq == "M":
        step = 1440
        unit = "Months"
    if freq == "A":
        step = 525600
        unit = "Years"
    if freq == "RP":
        step = 1
        unit = "Run Period"
    plt.xticks(
        arange(0, units_passed + 1, step), (arange(0, units_passed + 1, step) / step)
    )
    plt.xlabel(f"{unit} passed")
    plt.ylabel(f"{data_type} in {results_keys[0][2]}")
    plt.title(f"{data_type} results")
    return plt


# EOF (End-Of-File)
