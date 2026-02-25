"""Reads DesignBuilder EnergyPlus Output files."""

# libraries
# import matplotlib as mpl
import os
import sys
from json import dump

import matplotlib.pyplot as plt
from db_eplusout_reader import Variable, get_results
from db_eplusout_reader.constants import RP, TS, A, D, H, M
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
# print("Enter SQL file path")
# path = input()
# PATH_TO_FILE = r"/home/dani/DB/eplusout.sql"


def collect_temperature_results(path, freq):
    """Using db_eplusout_reader to extract temperature results from eplusout SQL file.

    Parameters
    ----------
    path
        location of sql file to be parsed
    freq
        frequency of the data collection

    Returns
    -------
    temp_results
        dictionary
        Raw ResultsDictionary object of file parsing.
    temp_results_keys
        list
        Location, description and units of temperatures.
    temp_results_values
        list
        Raw values of temperatures.
    """

    if freq == "TS":
        temp_results = get_results(
            path, variables=[Variable(None, None, "C")], frequency=TS
        )
    if freq == "H":
        temp_results = get_results(
            path, variables=[Variable(None, None, "C")], frequency=H
        )
    if freq == "D":
        temp_results = get_results(
            path, variables=[Variable(None, None, "C")], frequency=D
        )
    if freq == "M":
        temp_results = get_results(
            path, variables=[Variable(None, None, "C")], frequency=M
        )
    if freq == "A":
        temp_results = get_results(
            path, variables=[Variable(None, None, "C")], frequency=A
        )
    if freq == "RP":
        temp_results = get_results(
            path, variables=[Variable(None, None, "C")], frequency=RP
        )

    # casting to list so can be serialized to json object, just using values
    temp_results_values = list(temp_results.values())
    with open("temp_results_values.json", "w") as f:
        dump(temp_results_values, f, indent=4)

    # casting to list so can be serialied to json objects, just using headers/keys
    temp_results_keys = list(temp_results.keys())
    with open("temp_results_keys.json", "w") as f:
        dump(temp_results_keys, f, indent=4)

    return freq, temp_results_keys, temp_results_values


def plot_results(results_values, results_keys, data_type, freq):
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
    units_passed = len(results_values[0])
    time_units = list(range(units_passed))

    plt.figure(dpi=100)
    # enumerate through the headers to label each line
    for i, keys in enumerate(results_keys):
        plt.plot(
            time_units,
            results_values[i],
            label=f"{keys[0]} {keys[1]}",
        )  # plotting the data on the axes

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


# setting up front page class
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.path = 0
        self.frequency = 0

    def validate_path(self, value, instance):
        value = repr(value)[1:-1]
        value = value.strip()
        if "\\" in value or "/" in value:
            self.path = value
        else:
            self.ids.path_input.text = "Invalid file. Try again"
        return instance

    def update_slider(self, value):
        if value == 0:
            self.ids.frequency_label_value.text = "Time Step"
            self.frequency = "TS"
        if value == 1:
            self.ids.frequency_label_value.text = "Hourly"
            self.frequency = "H"
        if value == 2:
            self.ids.frequency_label_value.text = "Daily"
            self.frequency = "D"
        if value == 3:
            self.ids.frequency_label_value.text = "Monthly"
            self.frequency = "M"
        if value == 4:
            self.ids.frequency_label_value.text = "Annual"
            self.frequency = "A"
        if value == 5:
            self.ids.frequency_label_value.text = "Run Period"
            self.frequency = "RP"

    def plot_graph(self):
        freq, temp_results_keys, temp_results_values = collect_temperature_results(
            self.path, self.frequency
        )
        fig = plot_results(temp_results_values, temp_results_keys, "Temperature", freq)

        try:
            data_screen = self.manager.get_screen("data")
            if hasattr(data_screen, "update_canvas"):
                data_screen.update_canvas(fig)
        except Exception:
            pass

        self.manager.transition.direction = "left"
        self.manager.current = "data"


# setting up screen that shows the plotted data
class DataScreen(Screen):
    def __init__(self, **kwargs):
        super(DataScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        layout1 = BoxLayout(padding=5, orientation="horizontal", size_hint=(1, 0.2))

        # adding background
        with layout1.canvas.before:
            Color(rgba=(0.129, 0.149, 0.192, 1))
            self._header_rect = Rectangle(size=layout1.size, pos=layout1.pos)
        layout1.bind(
            size=lambda inst, val: setattr(self._header_rect, "size", val),
            pos=lambda inst, val: setattr(self._header_rect, "pos", val),
        )

        # assigning the plotted Kivy-compatible matplotlib graph to variable
        self.graph_container = BoxLayout(
            size_hint=(1, 0.8), pos_hint={"x": 0, "y": 0.2}
        )
        self.canvas_widget = None

        layout.add_widget(self.graph_container)
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

    def update_canvas(self, fig):
        if self.canvas_widget:
            self.graph_container.remove_widget(self.canvas_widget)
        self.canvas_widget = FigureCanvasKivyAgg(fig.gcf())
        self.graph_container.add_widget(self.canvas_widget)


# setting up app class from KivyApp for main app
class ResultsPlotterApp(App):
    def build(self):
        sm = ScreenManager()
        # default to sliding right for any screen change
        sm.transition.direction = "right"

        # update screens
        sm.remove_widget(HomeScreen(name="home"))
        sm.remove_widget(DataScreen(name="data"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(DataScreen(name="data"))

        return sm


# run the app
if __name__ == "__main__":
    if hasattr(sys, "_MEIPASS"):
        resource_add_path(os.path.join(sys._MEIPASS))
    ResultsPlotterApp().run()

# EOF (End-Of-File)
