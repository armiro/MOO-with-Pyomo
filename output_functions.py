"""define output functions based on pyomo model variables as inputs"""


def hardness_removal_efficiency(model):
    """
    Compute hardness removal efficiency function based on coded input variables with
    RSM-provided intercept and linear/interaction/quadratic coefficients
    :param model: pyomo concrete model object
    :return: float
    """
    intercept = 55.64
    linear_coefs = -8.78 * model.h_conc + 3.53 * model.s_conc + 12.28 * model.ph + \
                   3.07 * model.time + 3.09 * model.current
    interaction_coefs = -2.57 * model.h_conc * model.s_conc + 1.28 * model.h_conc * model.ph - \
                        1.85 * model.h_conc * model.time - 5.09 * model.h_conc * model.current + \
                        4.16 * model.s_conc * model.ph - 5.86 * model.s_conc * model.time - \
                        4.00 * model.s_conc * model.current - 5.39 * model.ph * model.time - \
                        5.15 * model.ph * model.current + 2.68 * model.time * model.current
    quadratic_coefs = 2.07 * (model.h_conc ** 2) + 2.17 * (model.s_conc ** 2) - \
                      0.27 * (model.ph ** 2) - 3.42 * (model.time ** 2) - \
                      2.72 * (model.current ** 2)
    return intercept + linear_coefs + interaction_coefs + quadratic_coefs


# dynamically set minimum and maximum possible values based on RSM experiments
setattr(hardness_removal_efficiency, 'min', 18.00)
setattr(hardness_removal_efficiency, 'max', 84.70)


def silica_removal_efficiency(model):
    """
    Compute silica removal efficiency function based on coded input variables with
    RSM-provided intercept and linear/interaction/quadratic coefficients
    :param model: pyomo concrete model object
    :return: float
    """
    intercept = 96.05
    linear_coefs = -0.0358 * model.h_conc + 2.73 * model.s_conc + 0.49 * model.ph - \
                   1.16 * model.time + 0.53 * model.current
    interaction_coefs = -0.53 * model.h_conc * model.s_conc - 0.65 * model.h_conc * model.ph + \
                        0.94 * model.h_conc * model.time - 0.089 * model.h_conc * model.current + \
                        0.5 * model.s_conc * model.ph + 0.61 * model.s_conc * model.time + \
                        0.71 * model.s_conc * model.current - 0.94 * model.ph * model.time + \
                        0.16 * model.ph * model.current - 0.18 * model.time * model.current
    quadratic_coefs = -0.19 * (model.h_conc ** 2) - 1.43 * (model.s_conc ** 2) - \
                      0.28 * (model.ph ** 2) + 0.6 * (model.time ** 2) - \
                      0.16 * (model.current ** 2)
    return intercept + linear_coefs + interaction_coefs + quadratic_coefs


# dynamically set minimum and maximum possible values based on RSM experiments
setattr(silica_removal_efficiency, 'min', 94.00)
setattr(silica_removal_efficiency, 'max', 97.60)


def operating_cost(model):
    """
    Compute operating cost function based on coded input variables with
    RSM-provided intercept and linear/interaction/quadratic coefficients
    :param model: pyomo concrete model object
    :return: float
    """
    intercept = 3.81
    linear_coefs = 0.12 * model.h_conc - 0.005 * model.s_conc - 0.034 * model.ph + \
                   1.3 * model.time + 1.4 * model.current
    interaction_coefs = -0.15 * model.h_conc * model.s_conc - 0.051 * model.h_conc * model.ph - \
                        0.27 * model.h_conc * model.time + 0.16 * model.h_conc * model.current + \
                        0.12 * model.s_conc * model.ph + 0.17 * model.s_conc * model.time + \
                        0.025 * model.s_conc * model.current - 0.094 * model.ph * model.time - \
                        0.15 * model.ph * model.current + 0.86 * model.time * model.current
    quadratic_coefs = -0.03 * (model.h_conc ** 2) - 0.025 * (model.s_conc ** 2) - \
                      0.14 * (model.ph ** 2) + 0.052 * (model.time ** 2) - \
                      0.28 * (model.current ** 2)
    return intercept + linear_coefs + interaction_coefs + quadratic_coefs


# dynamically set minimum and maximum possible values based on RSM experiments
setattr(operating_cost, 'min', 1.52)
setattr(operating_cost, 'max', 8.10)
