################################################################
# make_ORCA_seedfile_OSNAP_East.py
# --------------------------------------------------------------
# Description: Script to create seeding input file for
# TRACMASS simulations using ORCA NEMO model grids.
# This generates a seed .csv file for OSNAP East.
#
# Requirements: Model coordinates of the OSNAP line (West + East)
# must be provided in a .pkl file including the associated flux
# stored in the form "U+"/"U-"/"V+"/"V-" for zonal and meridional
# cells respectively.
# --------------------------------------------------------------
# Created On: 2022-07-19
# Created By: Ollie Tooth
# Email: oliver.tooth@seh.ox.ac.uk
###############################################################
# Import packages.
import os
import numpy as np
import pandas as pd

# Navigating to OSNAP extracted data directory.
# MODIFY: directory path.
os.chdir('PATH TO OSNAP .pkl FILE')

# --------------------------------------------------------------
# Read grid coordinates of OSNAP array from .pkl file.
# MODIFY: file name.
data = pd.read_pickle('osnap_line_ORCA.pkl')

# MODIFY: e_start corresponds to the index distinguishing OSNAP East
# from OSNAP West.
e_start = 28
# Extract i, j and volume flux values.
i_east = np.array([i[1] for i in data[e_start:]])
j_east = np.array([i[0] for i in data[e_start:]])
# String representation of volume flux passing INTO the basin.
flux_east = np.array([i[2] for i in data[e_start:]])

# Removing incorrect coordinates of OSNAP East plane.
# MODIFY: indexes to remove any incorrect coordinates.
i_east = np.delete(i_east, [])
j_east = np.delete(j_east, [])
flux_east = np.delete(flux_east, [])

# Initialise empty arrays to store seeding section (isec) and direction
# of fluxes to seed (idir).
nsteps = len(i_east)
isec_east = np.zeros(nsteps)
idir_east = np.zeros(nsteps)

# Translate string representation of fluxes into basin to numeric values
# stored in isec and idir arrays.

# Store isec value to specify the cell wall for release -
# (1) zonal, (2) meridional and (3) vertical.

# Store idir values to specify the direction to release particles -
# (1) flux > 0 and (-1) flux < 0.

# MODIFY: To seed water parcels on outflow (southward across OSNAP East)
# reverse sign of idir_west variable as noted below.

for i, val in enumerate(flux_east):
    if val == 'U-':
        # Zonal cell wall.
        isec_east[i] = 1
        # To seed flow out of the basin (use opposite sign to string rep.).
        idir_east[i] = -1

    elif val == 'U+':
        # Zonal cell wall.
        isec_east[i] = 1
        # To seed flow out of the basin (use opposite sign to string rep.).
        idir_east[i] = 1

    elif val == 'V+':
        # Meridional cell wall.
        isec_east[i] = 2
        # To seed flow out of the basin (use opposite sign to string rep.).
        idir_east[i] = 1

# Set number of depth levels.
k_len = 75

# Set upper and lower depth levels.
k_top = 0
k_bottom = 75

# Determine number of rows in final seeding file.
rows = len(isec_east) * k_len

# Setting number of columns [i, j, k, isec, idir].
cols = 5

# Configuire inital (1 x cols) empty array, seeds.
seeds = np.zeros([rows, cols])

# --------------------------------------------------------------
# Adding i indices for seeding.
seeds[:, 0] = np.repeat(i_east, k_len)

# Adding j indices for seeding.
seeds[:, 1] = np.repeat(j_east, k_len)

# Adding k indices for seeding.
seeds[:, 2] = list(np.arange(k_top, k_bottom)) * len(isec_east)

# Adding isec value to specify cell wall for release.
seeds[:, 3] = np.repeat(isec_east, k_len)

# Adding idir value to specify
seeds[:, 4] = np.repeat(idir_east, k_len)

# --------------------------------------------------------------
# Setting seeds array dtype to integers.
seeds = seeds.astype(int)

# --------------------------------------------------------------

# Combine np arrays into seed dictionary with keys: i, j, k, isec, idir.
seed = {'i': seeds[:, 0], 'j': seeds[:, 1], 'k': seeds[:, 2], 'isec': seeds[:, 3], 'idir': seeds[:, 4]}

# --------------------------------------------------------------

# Using a DataFrame to export seed dictionary to a .csv file with
# commas terminating each line.
# MODIFY: output filename as required.
filename = 'PATH TO OUTPUT FILE: ORCA_OSNAP_East_Inflow_seedfile.csv'
pd.DataFrame.from_dict(seed).to_csv(filename,
                                    header=None,
                                    index=None,
                                    line_terminator=',\n'
                                    )
