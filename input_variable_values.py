"""define input variable discrete values and lower/upper bounds"""

hardness_conc_values = [250, 437.5, 625, 812.5, 1000]
silica_conc_values = [5, 23.75, 42.5, 61.25, 80]
initial_ph_values = [3, 5, 7, 9, 11]
contact_time_values = [30, 45, 60, 75, 90]
current_density_values = [2.2, 4.425, 6.65, 8.875, 11.1]

coded_values = [-2.0, -1.0, 0.0, +1.0, +2.0]

hardness_conc_bounds = (min(hardness_conc_values), max(hardness_conc_values))
silica_conc_bounds = (min(silica_conc_values,), max(silica_conc_values))
initial_ph_bounds = (min(initial_ph_values), max(initial_ph_values))
contact_time_bounds = (min(contact_time_values), max(contact_time_values))
current_density_bounds = (min(current_density_values), max(current_density_values))

coded_bounds = (min(coded_values), max(coded_values))
