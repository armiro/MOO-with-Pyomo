"""
Multi-Objective Optimization using Pyomo with epsilon-constraint
Developed by Arman H. (https://github.com/armiro)
"""
# import random
import pyomo.environ as pyo
import matplotlib.pyplot as plt
import numpy as np

import output_functions as out_fns
import input_variable_values as in_vars


def plot_pareto_fronts(**objective_functions):
    """
    plot pareto-front plot as a scatter plot with num_optimal_solutions points
    :param objective_functions: kwargs containing a number of obj func names and values
    :return: None
    """
    names = list()
    of_values = list()
    for name, values in objective_functions.values():
        names.append(name)
        of_values.append(values)
    # fig = plt.figure(num=1)
    plt.scatter(of_values[1], of_values[2])
    plt.xlabel(names[1])
    plt.ylabel(names[2])
    plt.title("Pareto-Front Plot")
    plt.grid(True)
    plt.show()


# create a concrete Pyomo model
model = pyo.ConcreteModel(name='Pyomo Model')

# define the independent variables (raw values)
# model.h_conc = pyo.Var(bounds=in_vars.hardness_conc_bounds, domain=pyo.NonNegativeReals)
# model.s_conc = pyo.Var(bounds=in_vars.silica_conc_bounds, domain=pyo.NonNegativeReals)
# model.ph = pyo.Var(bounds=in_vars.initial_ph_bounds, domain=pyo.NonNegativeReals)
# model.time = pyo.Var(bounds=in_vars.contact_time_bounds, domain=pyo.NonNegativeReals)
# model.current = pyo.Var(bounds=in_vars.current_density_bounds, domain=pyo.NonNegativeReals)

# define the independent variables (coded values)
model.h_conc = pyo.Var(bounds=in_vars.coded_bounds, domain=pyo.NonNegativeReals)
model.s_conc = pyo.Var(bounds=in_vars.coded_bounds, domain=pyo.NonNegativeReals)
model.ph = pyo.Var(bounds=in_vars.coded_bounds, domain=pyo.NonNegativeReals)
model.time = pyo.Var(bounds=in_vars.coded_bounds, domain=pyo.NonNegativeReals)
model.current = pyo.Var(bounds=in_vars.coded_bounds, domain=pyo.NonNegativeReals)

# define output variables as expressions
model.hre = pyo.Expression(rule=out_fns.hardness_removal_efficiency, name='Hardness Removal Efficiency')
model.sre = pyo.Expression(rule=out_fns.silica_removal_efficiency, name='Silica Removal Efficiency')
model.oc = pyo.Expression(rule=out_fns.operating_cost, name='Operating Cost')

# define the objective functions (to be minimized/maximized)
model.o_hre = pyo.Objective(expr=model.hre, sense=pyo.maximize)
model.o_sre = pyo.Objective(expr=model.sre, sense=pyo.maximize)
model.o_oc = pyo.Objective(expr=model.oc, sense=pyo.minimize)

# create the solver instance
opt = pyo.SolverFactory('ipopt', executable='./optimizer/ipopt.exe')

# define the number of optimal solutions
NUM_OPTIMAL_SOLUTIONS = 30

# define epsilon range for each objective function (experimentally: min_of <= e <= max_of)
e_hre_range = (out_fns.hardness_removal_efficiency.min, out_fns.hardness_removal_efficiency.max)
e_sre_range = (out_fns.silica_removal_efficiency.min, out_fns.silica_removal_efficiency.max)
e_oc_range = (out_fns.operating_cost.min, out_fns.operating_cost.max)

# generate random epsilon values for each objective function
# e_hre_vals = [round(random.uniform(*e_hre_range), 2) for _ in range(NUM_OPTIMAL_SOLUTIONS)]
# e_sre_vals = [round(random.uniform(*e_sre_range), 2) for _ in range(NUM_OPTIMAL_SOLUTIONS)]
# e_oc_vals = [round(random.uniform(*e_oc_range), 2) for _ in range(NUM_OPTIMAL_SOLUTIONS)]

# generate epsilon values with similar distance for each objective function
e_hre_vals = np.arange(*e_hre_range, (e_hre_range[1]-e_hre_range[0])/NUM_OPTIMAL_SOLUTIONS)
e_sre_vals = np.arange(*e_sre_range, (e_sre_range[1]-e_sre_range[0])/NUM_OPTIMAL_SOLUTIONS)
e_oc_vals = np.arange(*e_oc_range, (e_oc_range[1]-e_oc_range[0])/NUM_OPTIMAL_SOLUTIONS)

# create a dictionary to store results
all_results = {}

# solve the epsilon-constraint problem for each objective function
for e_hre, e_sre, e_oc in zip(e_hre_vals, e_sre_vals, e_oc_vals):
    # fix one objective and optimize others
    model.e_constraint_hre = pyo.Constraint(expr=model.hre <= e_hre)
    model.e_constraint_sre = pyo.Constraint(expr=model.sre <= e_sre)
    model.e_constraint_oc = pyo.Constraint(expr=model.oc <= e_oc)

    # set the objective to be optimized (ONLY ONE can be set activated simultaneously)
    model.o_hre.deactivate()
    model.o_sre.deactivate()
    model.o_oc.activate()

    # solve the model using optimizer
    results = opt.solve(model, tee=True)

    # store the results in a dictionary
    all_results['hre=%.2f sre=%.2f oc=%.2f' % (e_hre, e_sre, e_oc)] = {
        "Objective 1 (hre)": pyo.value(model.o_hre),
        "Objective 2 (sre)": pyo.value(model.o_sre),
        "Objective 3 (oc)": pyo.value(model.o_oc),
        "Inputs (h_conc)": {h: pyo.value(model.h_conc[h]) for h in model.h_conc},
        "Inputs (s_conc)": {s: pyo.value(model.s_conc[s]) for s in model.s_conc},
        "Inputs (ph)": {ph: pyo.value(model.ph[ph]) for ph in model.ph},
        "Inputs (time)": {time: pyo.value(model.time[time]) for time in model.time},
        "Inputs (current)": {current: pyo.value(model.current[current]) for current in model.current}
    }

    # remove the epsilon constraints after each iteration
    model.del_component(model.e_constraint_hre)
    model.del_component(model.e_constraint_sre)
    model.del_component(model.e_constraint_oc)

# print the results
for e, result in all_results.items():
    print(f"Epsilon: {e}")
    for key, value in result.items():
        print(f"{key}: {value}")
    print("===" * 10)

# extract the objective values from all_results
obj1_values = [result['Objective 1 (hre)'] for result in all_results.values()]
obj2_values = [result['Objective 2 (sre)'] for result in all_results.values()]
obj3_values = [result['Objective 3 (oc)'] for result in all_results.values()]

# plot all pareto fronts using a scatter plot
plot_pareto_fronts(of1=(model.hre.getname(), obj1_values),
                   of2=(model.sre.getname(), obj2_values),
                   of3=(model.oc.getname(), obj3_values))


