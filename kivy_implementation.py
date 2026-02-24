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
from kivy.graphics import Color, Rectangle
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from numpy import arange

# usually ask for user input, however using example for now
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

    plt.figure(dpi=100)
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
    return plt


# setting up front page class
class HomeScreen(Screen):
    pass


# setting up screen that shows the plotted data
class DataScreen(Screen):
    def __init__(self, **kwargs):
        super(DataScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        layout1 = BoxLayout(padding=5, orientation="horizontal", size_hint=(1, 0.3))

        # adding background
        with layout1.canvas.before:
            Color(rgba=(0.129, 0.149, 0.192, 1))
            self._header_rect = Rectangle(size=layout1.size, pos=layout1.pos)
        layout1.bind(
            size=lambda inst, val: setattr(self._header_rect, "size", val),
            pos=lambda inst, val: setattr(self._header_rect, "pos", val),
        )

        # assigning the plotted Kivy-compatible matplotlib graph to variable
        plot = self.plot_graph()
        graph = FigureCanvasKivyAgg(plot.gcf())
        # ensure the graph fills the space above the bottom bar
        graph.size_hint = (1, 0.7)
        graph.pos_hint = {"x": 0, "y": 0.3}

        layout.add_widget(graph)
        layout1.add_widget(Label(text="Graph"))
        layout1.add_widget(
            Button(
                text="Back",
                on_press=lambda inst: (
                    setattr(self.manager.transition, "direction", "right")
                    or setattr(self.manager, "current", "home")
                ),
            )
        )

        layout.add_widget(layout1)

        self.add_widget(layout)

    def plot_graph(self):
        temperature_results, temperature_result_keys, temperature_result_values = (
            collect_temperature_results(PATH_TO_FILE)
        )
        plot = plot_results(
            temperature_result_values, temperature_result_keys, "Temperature"
        )
        return plot


# setting up app class from KivyApp for main app
class ResultsPlotterApp(App):
    def build(self):
        sm = ScreenManager()
        # default to sliding right for any screen change
        sm.transition.direction = "right"
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(DataScreen(name="data"))

        return sm


# run the app
if __name__ == "__main__":
    if hasattr(sys, "_MEIPASS"):
        resource_add_path(os.path.join(sys._MEIPASS))
    ResultsPlotterApp().run()

# EOF (End-Of-File)
