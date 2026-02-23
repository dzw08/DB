"""Reads DesignBuilder EnergyPlus Output files."""

# libraries
from db_eplusout_reader import Variable, DBEsoFile, get_results
from db_eplusout_reader.constants import RP, H
import tkinter as tk
import matplotlib as mpl

# parse output file, usually ask for user input, however using example for now

#print("Enter eso file path")
#path = input()
path = r"/home/dani/DB/eplusout.sql"
temperature_results = get_results(path, variables=[Variable(None,None,"C")], frequency=H)
print(temperature_results)