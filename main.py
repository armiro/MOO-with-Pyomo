"""
Multi-Objective Optimization using Pyomo with epsilon-constraint
Developed by Arman H. (https://github.com/armiro)
"""
# import random
import csv
import pyomo.environ as pyo
import matplotlib.pyplot as plt
import numpy as np
import output_functions as out_fns
import input_variable_values as in_vars


# define global constant variables
OPTIMIZER = 'ipopt'
OPT_PATH = './optimizer/ipopt.exe'
RESULT_PATH = './results/'
CSV_FILE_PATH = RESULT_PATH + 'optimal_solutions.csv'
NUM_OPTIMAL_SOLUTIONS = 30  # same as number of epsilons


def plot_pareto_fronts(target_name, **objective_functions):
    """
    plot pareto-front plot as a scatter plot with num_optimal_solutions points
    :param target_name: string, name of the function to set as y-axis
    :param objective_functions: kwargs, a number of obj func names and values
    :return: None
    """
    of_names = []
    of_values_list = []
    for name, values in objective_functions.values():
        if name is target_name:
            target_values = values
        else:
            of_names.append(name)
            of_values_list.append(values)

    for of_name, of_values in zip(of_names, of_values_list):
        plt.clf()
        plt.scatter(of_values, target_values)
        plt.xlabel(of_name)
        plt.ylabel(target_name)
        plt.title('Pareto-Front Plot')
        plt.grid(True)
        plt.savefig(fname=f"{RESULT_PATH}/pareto_front_"
                          f"{''.join(l[0] for l in target_name.split())}_"
                          f"{''.join(l[0] for l in of_name.split())}.png")
    plt.clf()
    plt.scatter(of_values_list[0], of_values_list[1])
    plt.xlabel(of_names[0])
    plt.ylabel(of_names[1])
    plt.title('Pareto-Front Plot')
    plt.grid(True)
    plt.savefig(fname=f"{RESULT_PATH}/pareto_front_"
                      f"{''.join(l[0] for l in of_names[0].split())}_"
                      f"{''.join(l[0] for l in of_names[1].split())}.png")


def write_to_csv(filename, row):
    """
    write the input row as the last row of a CSV file
    :param filename: CSV file path
    :param row: list of input values
    :return: None
    """
    with open(filename, mode='a', newline='', encoding='utf-8') as csv_file:
        csv.writer(csv_file).writerow(row)


def find_active_obj_fn_from(*obj_fns):
    """
    find the first active objective function from the input list of functions
    :param obj_fns: args, a number of objective functions
    :return: pyomo objective function
    :raises ValueError: if none of the functions are active
    """
    for obj_fn in obj_fns:
        if obj_fn.active:
            return obj_fn.expr.doc
    raise ValueError("None of the objective functions are activated.")


def set_obj_fn_boundaries(*expressions, optimizer, pyo_model):
    """
    extract possible optimum (min/max) values for each output function. values are set as
    attributes for model expressions to later set boundaries of epsilon values
    :param expressions: pyomo expressions (output functions)
    :param optimizer: pyomo solver (e.g. IPOPT)
    :param pyo_model: pyomo concrete model
    :return: None
    """
    for expr in expressions:
        for sense in [pyo.maximize, pyo.minimize]:
            pyo_model.obj_fn = pyo.Objective(expr=expr, sense=sense)
            pyo_model.obj_fn.activate()
            optimizer.solve(pyo_model, tee=True)
            expr_optimum = pyo.value(pyo_model.obj_fn)
            setattr(expr, 'min' if sense == pyo.minimize else 'max', expr_optimum)
            pyo_model.del_component(name_or_object='obj_fn')


def main():
    """
    define pyomo model, initialize inputs and functions, define epsilon constraint method,
    use optimizer to solve multiple functions (multiple single-objective functions)
    provide an excel file of NUM_OPTIMAL_SOLUTIONS rows each representing an optimal solution
    draw pareto-front plots for all each combination of objective functions as x-y axis
    :return: None
    """
    # create a concrete Pyomo model
    model = pyo.ConcreteModel(name='Pyomo Model')

    # define the independent variables (raw values)
    model.h_conc = pyo.Var(bounds=in_vars.hardness_conc_bounds, domain=pyo.NonNegativeReals)
    model.s_conc = pyo.Var(bounds=in_vars.silica_conc_bounds, domain=pyo.NonNegativeReals)
    model.ph = pyo.Var(bounds=in_vars.initial_ph_bounds, domain=pyo.NonNegativeReals)
    model.time = pyo.Var(bounds=in_vars.contact_time_bounds, domain=pyo.NonNegativeReals)
    model.current = pyo.Var(bounds=in_vars.current_density_bounds, domain=pyo.NonNegativeReals)

    # define the independent variables (coded values)
    # model.h_conc = pyo.Var(bounds=in_vars.coded_bounds, domain=pyo.Reals)
    # model.s_conc = pyo.Var(bounds=in_vars.coded_bounds, domain=pyo.Reals)
    # model.ph = pyo.Var(bounds=in_vars.coded_bounds, domain=pyo.Reals)
    # model.time = pyo.Var(bounds=in_vars.coded_bounds, domain=pyo.Reals)
    # model.current = pyo.Var(bounds=in_vars.coded_bounds, domain=pyo.Reals)

    # define outputs as expressions (using 'rule' instead of 'expr' to handle complex expressions)
    model.hre = pyo.Expression(rule=out_fns.hardness_removal_efficiency,
                               doc='Hardness Removal Efficiency')
    model.sre = pyo.Expression(rule=out_fns.silica_removal_efficiency,
                               doc='Silica Removal Efficiency')
    model.oc = pyo.Expression(rule=out_fns.operating_cost,
                              doc='Operating Cost')

    # create the solver instance
    opt = pyo.SolverFactory(OPTIMIZER, executable=OPT_PATH, solver_io='nl')

    # find boundaries of each objective function by solving single-objective problem and
    # define epsilon range for each objective function using calculated optimum values
    set_obj_fn_boundaries(model.hre, model.sre, model.oc, optimizer=opt, pyo_model=model)
    e_hre_range = (model.hre.min, model.hre.max)
    e_sre_range = (model.sre.min, model.sre.max)
    e_oc_range = (model.oc.min, model.oc.max)

    # generate random epsilon values for each objective function
    # e_hre_vals = [round(random.uniform(*e_hre_range), 2) for _ in range(NUM_OPTIMAL_SOLUTIONS)]
    # e_sre_vals = [round(random.uniform(*e_sre_range), 2) for _ in range(NUM_OPTIMAL_SOLUTIONS)]
    # e_oc_vals = [round(random.uniform(*e_oc_range), 2) for _ in range(NUM_OPTIMAL_SOLUTIONS)]

    # generate epsilon values with similar distance for each objective function
    e_hre_vals = np.arange(*e_hre_range, (e_hre_range[1] - e_hre_range[0]) / NUM_OPTIMAL_SOLUTIONS)
    e_sre_vals = np.arange(*e_sre_range, (e_sre_range[1] - e_sre_range[0]) / NUM_OPTIMAL_SOLUTIONS)
    e_oc_vals = np.arange(*e_oc_range, (e_oc_range[1] - e_oc_range[0]) / NUM_OPTIMAL_SOLUTIONS)

    # define the objective functions (to be minimized/maximized)
    model.o_hre = pyo.Objective(expr=model.hre, sense=pyo.maximize)
    model.o_sre = pyo.Objective(expr=model.sre, sense=pyo.maximize)
    model.o_oc = pyo.Objective(expr=model.oc, sense=pyo.minimize)

    # create a dictionary to store results
    all_results = {}

    # solve the epsilon-constraint problem for each objective function
    for e_hre, e_sre, e_oc in zip(e_hre_vals, e_sre_vals, e_oc_vals):
        # fix one objective and optimize others
        model.e_constraint_hre = pyo.Constraint(expr=model.hre <= e_hre)
        model.e_constraint_sre = pyo.Constraint(expr=model.sre <= e_sre)
        model.e_constraint_oc = pyo.Constraint(expr=model.oc <= e_oc)

        # set the objective to be optimized (ONLY ONE can be set activated simultaneously)
        model.o_hre.activate()
        model.o_sre.deactivate()
        model.o_oc.deactivate()

        # solve the model using optimizer
        opt.solve(model, tee=True)

        # store the results in a dictionary
        all_results[f'e_hre={e_hre:.2f} e_sre={e_sre:.2f} e_oc={e_oc:.2f}'] = {
            "OF1 (hre)": round(pyo.value(model.o_hre), ndigits=2),
            "OF2 (sre)": round(pyo.value(model.o_sre), ndigits=2),
            "OF3 (oc)": round(pyo.value(model.o_oc), ndigits=2),
            "X1 (h_conc)": round(pyo.value(model.h_conc), ndigits=2),
            "X2 (s_conc)": round(pyo.value(model.s_conc), ndigits=2),
            "X3 (ph)": round(pyo.value(model.ph), ndigits=2),
            "X4 (time)": round(pyo.value(model.time), ndigits=2),
            "X5 (current)": round(pyo.value(model.current), ndigits=2)
        }

        # remove the epsilon constraints after each iteration
        model.del_component(model.e_constraint_hre)
        model.del_component(model.e_constraint_sre)
        model.del_component(model.e_constraint_oc)

    # initialize the CSV file with header
    header_row = ['Solution No.', 'X1 (mg/L)', 'X2 (mg/L)', 'X3', 'X4 (min)', 'X5 (mA/cm2)',
                  'OF1 (%)', 'OF2 (%)', 'OF3 (USD/m3)']
    write_to_csv(filename=CSV_FILE_PATH, row=header_row)

    # print the results and write each row to CSV file
    for idx, (eps, result) in enumerate(all_results.items()):
        print(f"Solution No. {idx + 1} | Epsilon: {eps}")
        for key, value in result.items():
            print(f"{key}: {value}")
        write_to_csv(filename=CSV_FILE_PATH,
                     row=[idx + 1, result['X1 (h_conc)'], result['X2 (s_conc)'], result['X3 (ph)'],
                          result['X4 (time)'], result['X5 (current)'],
                          result['OF1 (hre)'], result['OF2 (sre)'], result['OF3 (oc)']])
        print("=" * 50)

    # extract the objective values from all_results
    obj1_values = [result['OF1 (hre)'] for result in all_results.values()]
    obj2_values = [result['OF2 (sre)'] for result in all_results.values()]
    obj3_values = [result['OF3 (oc)'] for result in all_results.values()]

    # plot all pareto fronts using a scatter plot
    target_of_name = find_active_obj_fn_from(model.o_hre, model.o_sre, model.o_oc)
    plot_pareto_fronts(target_name=target_of_name,
                       of1=(model.hre.doc, obj1_values),
                       of2=(model.sre.doc, obj2_values),
                       of3=(model.oc.doc, obj3_values))


if __name__ == '__main__':
    main()
