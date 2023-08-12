"""define input variable discrete values and lower/upper bounds"""

hardness_conc_values = [250, 437.5, 625, 812.5, 1000]
silica_conc_values = [5, 23.75, 42.5, 61.25, 80]
initial_ph_values = [3, 5, 7, 9, 11]
contact_time_values = [30, 45, 60, 75, 90]
current_density_values = [2.2, 4.425, 6.65, 8.875, 11.1]

coded_values = [-2.0, -1.0, 0.0, +1.0, +2.0]

hardness_conc_bounds = (hardness_conc_values[1], hardness_conc_values[-2])
silica_conc_bounds = (silica_conc_values[1], silica_conc_values[-2])
initial_ph_bounds = (initial_ph_values[1], initial_ph_values[-2])
contact_time_bounds = (contact_time_values[1], contact_time_values[-2])
current_density_bounds = (current_density_values[1], current_density_values[-1])

coded_bounds = (min(coded_values), max(coded_values))
