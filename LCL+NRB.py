import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import csv

def julian_to_datetime(julian_time):
    reference_date = datetime(1858, 11, 17)
    days = julian_time - 2400000.5
    modern_date = reference_date + timedelta(days=days)
    return modern_date

file_path = '/Users/B2/Downloads/cbh/MPLNET_V3_L15_NRB_20200201_MPL44258_GSFC .nc4'
ds = nc.Dataset(file_path)

# Access the 'nrb' and 'altitude' variables
if 'nrb' in ds.variables and 'altitude' in ds.variables:
    nrb_variable = ds.variables['nrb'][0, :, :]  # Adjust indices as needed
    altitude_variable = ds.variables['altitude'][:]
    time_variable = ds.variables['time'][:]

    # Convert Julian time to modern date
    modern_dates = [julian_to_datetime(julian_time) for julian_time in time_variable]

    # Masked array (set masked values to NaN)
    nrb_variable[nrb_variable <= 0] = np.nan

    # Create a plot using modern dates on the x-axis
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(modern_dates, altitude_variable[0, :], nrb_variable.T, cmap='viridis', shading='auto', vmax=5)
    cbar = plt.colorbar()

    plt.ylim(0, 7)
    plt.xlabel('Date')
    plt.ylabel('Altitude')
    plt.title('NRB vs. Altitude')

    # Overlay LCL line on the plot
    with open('lcl_output_hourly.csv', 'r') as lcl_file:
        reader = csv.reader(lcl_file)
        next(reader)  # Skip header
        lcl_data = list(reader)
    
    hours = [int(row[0]) for row in lcl_data]
    lcl_values = [float(row[1]) for row in lcl_data]

    plt.plot(modern_dates[hours], lcl_values, marker='o', linestyle='-', color='red', label='LCL')

    # Show legend
    plt.legend()

    # Show the plot
    plt.show()
