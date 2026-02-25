"""Reads DesignBuilder EnergyPlus Output files."""

# libraries
import os
import sys

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from no_gui import collect_temperature_results, plot_results


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.path = 0
        self.frequency = 0
        self.legend = False

    def legend_query(self, state):
        if state == "down":
            self.ids.legend_button.text = "ON"
            self.legend = True
        else:
            self.ids.legend_button.text = "OFF"
            self.legend = False

    def validate_path(self, value, instance):
        value = repr(value)[1:-1]
        value = value.strip()
        if ("\\" in value or "/" in value) and ".sql" in value[-4:]:
            self.path = value
        else:
            self.ids.path_input.text = "Invalid file. Try again"

        return instance

    def update_slider(self, value):
        match value:
            case 0:
                self.ids.frequency_label_value.text = "Time Step"
                self.frequency = "TS"
            case 1:
                self.ids.frequency_label_value.text = "Hourly"
                self.frequency = "H"
            case 2:
                self.ids.frequency_label_value.text = "Daily"
                self.frequency = "D"
            case 3:
                self.ids.frequency_label_value.text = "Monthly"
                self.frequency = "M"
            case 4:
                self.ids.frequency_label_value.text = "Annual"
                self.frequency = "A"
            case 5:
                self.ids.frequency_label_value.text = "Run Period"
                self.frequency = "RP"

    def plot_graph(self):
        try:
            freq, temp_results_keys, temp_results_values = collect_temperature_results(
                self.path, self.frequency
            )
            fig = plot_results(
                temp_results_values, temp_results_keys, "Temperature", freq
            )
        except (UnboundLocalError, TypeError, OSError):
            error_message_path = ModalView(
                auto_dismiss=False, background_color=[0, 0, 0, 0.6]
            )

            content = FloatLayout()

            holder = BoxLayout(
                padding=5,
                orientation="vertical",
                size_hint=(0.5, 0.2),
                pos_hint={"x": 0.25, "y": 0.4},
            )
            holder.add_widget(
                Label(
                    text="Error! Please enter valid path to SQL file",
                    color=[1, 0.29, 0.31, 1],
                )
            )
            close = Button(text="Dismiss")
            holder.add_widget(close)

            content.add_widget(holder)
            error_message_path.add_widget(content)

            close.bind(on_press=error_message_path.dismiss)
            error_message_path.open()
        except IndexError:
            error_message_frequency = ModalView(
                auto_dismiss=False, background_color=[0, 0, 0, 0.6]
            )

            content = FloatLayout()

            holder = BoxLayout(
                padding=5,
                orientation="vertical",
                size_hint=(0.5, 0.2),
                pos_hint={"x": 0.25, "y": 0.4},
            )
            holder.add_widget(
                Label(
                    text="Error! Please enter correct output interval frequency.",
                    color=[1, 0.29, 0.31, 1],
                )
            )
            close = Button(text="Dismiss")
            holder.add_widget(close)

            content.add_widget(holder)
            error_message_frequency.add_widget(content)

            close.bind(on_press=error_message_frequency.dismiss)
            error_message_frequency.open()

        try:
            if self.legend:
                fig.legend()
        except UnboundLocalError:
            pass

        try:
            data_screen = self.manager.get_screen("data")
            if hasattr(data_screen, "update_canvas"):
                data_screen.update_canvas(fig)
            self.manager.transition.direction = "left"
            self.manager.current = "data"
        except Exception:
            pass


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
