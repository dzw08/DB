"""Reads DesignBuilder EnergyPlus Output files."""

# libraries
from db_eplusout_reader import Variable, DBEsoFile, get_results
from db_eplusout_reader.constants import RP, H
import tkinter as tk
import matplotlib as mpl

# parse eso file, usually ask for user input, however using example for now

#print("Enter eso file path")
#path = input()
path = r"/home/dani/DB/eplusout.eso"
eso = DBEsoFile.from_path(path)  
