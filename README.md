# DB EnergyPlus SQL Temperature Reader

![Python badge](https://img.shields.io/badge/python-3.13_%7C_3.14-blue "compatible for Python >= 3.13.4")

***

Python [Kivy](https://kivy.org/)-based GUI tool to plot temperature results from EnergyPlus output files (```.sql```) using [`db-eplusout-reader`](https://github.com/DesignBuilderSoftware/db-eplusout-reader) and [`matplotlib`](https://matplotlib.org/).

## Functionality

- Takes ```.sql``` (SQLite) output files from EnergyPlus and extracts temperature values.
- Reads results and plots them using `matplotlib` into a line graph.

## Usage

- Save ```.sql``` EnergyPlus output file into repo directory.

### To display data:

1. Run ```main.py``` and enter the file path into the text box.

![Input file path](assets/readme/file_path.png "File path input")

2. Enter data output interval using the slider, using one of `TS` (timestep), `H` (hourly), `D` (daily), `M` (monthly), `A` (annual), or `RP` (runperiod).

![Interval of data output](assets/readme/data_interval.png "Interval of data output")

3. Select whether you would like a `legend`.

![Legend](assets/readme/legend.png "Legend")

---

> To run the sample file, use file path
> 
> **For MacOS and Linux**: ```./sample_sql_files/eplusout_hourly.sql```
>
> **For Windows**: ```.\sample_sql_files\eplusout_hourly.sql```
>
> And select data interval `Hourly`.

---

### Output

4. Click the `show results` button.
5. This will take you to a secondary screen that should display like this:

![Output graph](assets/readme/output.png "Output graph")


## Installation

### Inital setup

Use [uv](https://github.com/astral-sh/uv) to install required dependencies.

```bash
# Install dependencies
uv sync --group dev

# Run tests
uv run pytest tests -v
```

### Run main.py

Ensure you are in repo directory and run:

```bash
python main.py
```

## Dependencies

| Dependency             | Version | Use                                       |
|------------------------|---------|-------------------------------------------|
| [`db-eplusout-reader`](https://github.com/DesignBuilderSoftware/db-eplusout-reader)     | 0.4.0   | Allows reading of eplusout SQL files      |
| [`kivy`](https://kivy.org)                   | 3.13    | Provides GUI                              |
| [`kivy-garden`](https://kivy.org/doc/stable/api-kivy.garden.html)            | 0.1.5   | Allows for matplotlib integration in kivy |
| [`kivy-garden-matplotlib`](https://github.com/kivy-garden/matplotlib) <br> _Note this flower requires `distutils` which was removed in Python 3.12+, so use [`setuptools`](https://github.com/pypa/setuptools) instead_ | 0.1.1   | Allows for matplotlib integration in kivy |
| [`matplotlib`](https://github.com/matplotlib/matplotlib)             | 3.10.8  | Plots the line graph with given data      |