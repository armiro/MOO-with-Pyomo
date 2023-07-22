import numpy as np
import pyomo.environ as pyo
import output_functions as out_fns
import random
import matplotlib.pyplot as plt



def plot_pareto_front(of1_values, of1_name, of2_values, of2_name):
    fig = plt.figure(num=1)
    plt.scatter(of1_values, of2_values)
    plt.xlabel(of1_name)
    plt.ylabel(of2_name)
    plt.title("Pareto-Front Plot")
    plt.grid(True)
    plt.show()


# create a concrete Pyomo model
model = pyo.ConcreteModel(name='Pyomo Model')

# define the independent variables
# model.h_conc = pyo.Var(bounds=(250.0, 1000.0), domain=pyo.NonNegativeReals, initialize=250.0)
# model.s_conc = pyo.Var(bounds=(5.0, 80.0), domain=pyo.NonNegativeReals, initialize=5.0)
# model.ph = pyo.Var(bounds=(3.0, 11.0), domain=pyo.NonNegativeReals, initialize=3.0)
# model.time = pyo.Var(bounds=(30.0, 90.0), domain=pyo.NonNegativeReals, initialize=30.0)
# model.current = pyo.Var(bounds=(2.2, 11.1), domain=pyo.NonNegativeReals, initialize=2.2)

model.h_conc = pyo.Var(bounds=(-2.0, 2.0), domain=pyo.NonNegativeReals)
model.s_conc = pyo.Var(bounds=(-2.0, 2.0), domain=pyo.NonNegativeReals)
model.ph = pyo.Var(bounds=(-2.0, 2.0), domain=pyo.NonNegativeReals)
model.time = pyo.Var(bounds=(-2.0, 2.0), domain=pyo.NonNegativeReals)
model.current = pyo.Var(bounds=(-2.0, 2.0), domain=pyo.NonNegativeReals)

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
num_optimal_solutions = 30

# define epsilon value ranges for each objective function (experimentally)
hre_epsilon_range = (2, 10)
sre_epsilon_range = (0.2, 1)
oc_epsilon_range = (0.5, 2)

# generate random epsilon values for each objective function
e_hre_vals = [round(random.uniform(*hre_epsilon_range), 2) for _ in range(num_optimal_solutions)]
e_sre_vals = [round(random.uniform(*sre_epsilon_range), 2) for _ in range(num_optimal_solutions)]
e_oc_vals = [round(random.uniform(*oc_epsilon_range), 2) for _ in range(num_optimal_solutions)]

# create a dictionary to store results
all_results = {}

# solve the epsilon-constraint problem for each objective function
for e_hre, e_sre, e_oc in zip(e_hre_vals, e_sre_vals, e_oc_vals):
    # fix one objective and optimize others
    model.e_constraint_hre = pyo.Constraint(expr=(model.hre <= e_hre))
    model.e_constraint_sre = pyo.Constraint(expr=(model.sre <= e_sre))
    model.e_constraint_oc = pyo.Constraint(expr=(model.oc <= e_oc))

    # Set the active objective to be maximized/minimized
    model.o_hre.activate()
    model.o_sre.deactivate()
    model.o_oc.deactivate()

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

for e, result in all_results.items():
    print(f"Epsilon: {e}")
    for key, value in result.items():
        print(f"{key}: {value}")
    print("=" * 30)

# Extract the objective values from all_results
objective1_values = [result['Objective 1 (hre)'] for result in all_results.values()]
objective2_values = [result['Objective 2 (sre)'] for result in all_results.values()]

# Plot the Pareto front using a scatter plot
plot_pareto_front(of1_values=objective1_values, of1_name=model.hre.getname(),
                  of2_values=objective2_values, of2_name=model.sre.getname())

