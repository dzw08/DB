"""Reads DesignBuilder EnergyPlus Output files."""

# libraries
# import matplotlib as mpl
import os
import sys
from json import dump

import matplotlib.pyplot as plt
from db_eplusout_reader import Variable, get_results
from db_eplusout_reader.constants import H
from kivy.app import App
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from numpy import arange

# parse output file, usually ask for user input, however using example for now

# print("Enter eso file path")
# path = input()
PATH_TO_FILE = r"/home/dani/DB/eplusout.sql"


def collect_temperature_results(path):
    """Using db_eplusout_reader to extract temperature results from eplusout SQL file.

    Parameters
    ----------
    path
        location of sql file to be parsed

    Returns
    -------
    temp_results
        dictionary
        Raw Results object of file parsing.
    temp_results_keys
        list
        Location, description and units of temperatures.
    temp_results_values
        list
        Raw values of temperatures.
    """
    temp_results = get_results(path, variables=[Variable(None, None, "C")], frequency=H)

    # casting to list so can be serialized to json object, just using values
    temp_results_values = list(temp_results.values())
    with open("temp_results_values.json", "w") as f:
        dump(temp_results_values, f, indent=4)

    # casting to list so can be serialied to json objects, just using headers/keys
    temp_results_keys = list(temp_results.keys())
    with open("temp_results_keys.json", "w") as f:
        dump(temp_results_keys, f, indent=4)

    return temp_results, temp_results_keys, temp_results_values


def plot_results(results_values, results_keys, data_type):
    """Plots db-eplusout-reader output files in a line graph using matplotlib.

    Parameters
    ----------
    results_values
        ARRAY The actual values of the data.
    results_keys
        ARRAY What the values of the data refer to as well as their units.
    data_type
        STR What kind of data, e.g. Temperature or energy

    Returns
    -------
    Plotted matplotlib data
    """
    # plot the results using matplotlib
    hours_passed = len(results_values[0])
    hours = []
    for i in range(hours_passed):
        hours.append(i)

    plt.figure(figsize=(10, 6), dpi=100, layout="constrained")
    # enumerate through the headers to label each line
    for i, keys in enumerate(results_keys):
        plt.plot(
            hours,
            results_values[i],
            label=f"{keys[0]} {keys[1]}",
        )  # plotting the data on the axes

    # labels
    plt.xticks(arange(0, hours_passed + 1, 24))
    plt.xlabel("Hours passed")
    plt.ylabel(f"{data_type} in {results_keys[0][2]}")
    plt.title(f"{data_type} results")
    plt.legend()
    return plt


# example usage
temperature_results, temperature_result_keys, temperature_result_values = (
    collect_temperature_results(PATH_TO_FILE)
)
plot = plot_results(temperature_result_values, temperature_result_keys, "Temperature")


# setting up front page class
class FrontPage(BoxLayout):
    def __init__(self, **kwargs):
        super(FrontPage, self).__init__(**kwargs)
        self.orientation = "horizontal"
        title_label = Label(text="Results Plotter")
        self.add_widget(title_label)
        self.add_widget(Button(label="hello"))


# setting up app class from KivyApp for main app
class ResultsPlotterApp(App):
    def build(self):
        return FrontPage()


# run the app
if __name__ == "__main__":
    if hasattr(sys, "_MEIPASS"):
        resource_add_path(os.path.join(sys._MEIPASS))
    ResultsPlotterApp().run()

# EOF (End-Of-File)
