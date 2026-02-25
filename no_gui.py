"""Collect and plots DB eplusout SQL data without going through GUI"""

# libraries
from eplusout_tools import collect_temperature_results, plot_results

# query file path
print("Enter eplusout SQL file path:")
verified = False
while not verified:
    path_to_file = input()
    path_to_file = repr(path_to_file)[1:-1].strip()
    if ("\\" in path_to_file or "/" in path_to_file) and ".sql" in path_to_file[-4:]:
        verified = True
    else:
        print("Invalid file path. Try again.")

# query legend
print("Legend?\n1. Yes\n2. No")
verified = False
while not verified:
    legend = input()
    try:
        match int(legend):
            case 1:
                print("Legend selected.")
                legend = True
                verified = True
            case 2:
                print("Legend deselected.")
                legend = False
                verified = True
            case _:
                raise ValueError
    except ValueError:
        print("Please enter 1 or 2")
        verified = False

# query frequency
print("Data Frequency?")
print("1. Time Step\n2. Hourly\n3. Daily\n4. Monthly\n5. Annually\n6. Run Period")
verified = False
while not verified:
    frequency = input()
    try:
        match int(frequency):
            case 1:
                frequency = "TS"
                verified = True
            case 2:
                frequency = "H"
                verified = True
            case 3:
                frequency = "D"
                verified = True
            case 4:
                frequency = "M"
                verified = True
            case 5:
                frequency = "A"
                verified = True
            case 6:
                frequency = "RP"
                verified = True
            case _:
                raise ValueError
    except ValueError:
        print("Please enter number from 1-6")
        verified = False

# plot results using data
freq, temp_results_keys, temp_results_values = collect_temperature_results(
    path_to_file, frequency
)
fig = plot_results(temp_results_values, temp_results_keys, "Temperature", frequency)
if legend:
    fig.legend()
fig.show()

# EOF (End-Of-File)
