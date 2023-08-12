"""define output functions based on pyomo model variables as inputs"""


# def hardness_removal_efficiency(model):
#     """
#     Compute hardness removal efficiency function based on coded input variables with
#     RSM-provided intercept and linear/interaction/quadratic coefficients
#     :param model: pyomo concrete model object
#     :return: float
#     """
#     intercept = 55.64
#     linear_coefs = -8.78 * model.h_conc + 3.53 * model.s_conc + 12.28 * model.ph \
#                    + 3.07 * model.time + 3.09 * model.current
#     inter_coefs = -2.57 * model.h_conc * model.s_conc + 1.28 * model.h_conc * model.ph \
#                   - 1.85 * model.h_conc * model.time - 5.09 * model.h_conc * model.current \
#                   + 4.16 * model.s_conc * model.ph - 5.86 * model.s_conc * model.time \
#                   - 4.00 * model.s_conc * model.current - 5.39 * model.ph * model.time \
#                   - 5.15 * model.ph * model.current + 2.68 * model.time * model.current
#     quad_coefs = 2.07 * (model.h_conc ** 2) + 2.17 * (model.s_conc ** 2) \
#                  - 0.27 * (model.ph ** 2) - 3.42 * (model.time ** 2) \
#                  - 2.72 * (model.current ** 2)
#     return intercept + linear_coefs + inter_coefs + quad_coefs


def hardness_removal_efficiency(model):
    """
    Compute hardness removal efficiency function based on coded input variables with
    RSM-provided intercept and linear/interaction/quadratic coefficients
    :param model: pyomo concrete model object
    :return: float
    """
    intercept = -260.31202
    linear_coefs = 0.007559 * model.h_conc + 1.23314 * model.s_conc + 18.71764 * model.ph \
                   + 4.05005 * model.time + 23.68839 * model.current
    inter_coefs = -0.000732 * model.h_conc * model.s_conc + 0.003402 * model.h_conc * model.ph \
                  - 0.000658 * model.h_conc * model.time - 0.012197 * model.h_conc * model.current \
                  + 0.111020 * model.s_conc * model.ph - 0.020847 * model.s_conc * model.time \
                  - 0.095898 * model.s_conc * model.current - 0.179609 * model.ph * model.time \
                  - 1.15747 * model.ph * model.current + 0.080172 * model.time * model.current
    quad_coefs = 0.000059 * (model.h_conc ** 2) + 0.006164 * (model.s_conc ** 2) \
                 - 0.067616 * (model.ph ** 2) - 0.015202 * (model.time ** 2) \
                 - 0.549520 * (model.current ** 2)
    return intercept + linear_coefs + inter_coefs + quad_coefs


# def silica_removal_efficiency(model):
#     """
#     Compute silica removal efficiency function based on coded input variables with
#     RSM-provided intercept and linear/interaction/quadratic coefficients
#     :param model: pyomo concrete model object
#     :return: float
#     """
#     intercept = 96.05
#     linear_coefs = -0.0358 * model.h_conc + 2.73 * model.s_conc + 0.49 * model.ph \
#                    - 1.16 * model.time + 0.53 * model.current
#     inter_coefs = -0.53 * model.h_conc * model.s_conc - 0.65 * model.h_conc * model.ph \
#                   + 0.94 * model.h_conc * model.time - 0.089 * model.h_conc * model.current \
#                   + 0.5 * model.s_conc * model.ph + 0.61 * model.s_conc * model.time \
#                   + 0.71 * model.s_conc * model.current - 0.94 * model.ph * model.time \
#                   + 0.16 * model.ph * model.current - 0.18 * model.time * model.current
#     quad_coefs = -0.19 * (model.h_conc ** 2) - 1.43 * (model.s_conc ** 2) \
#                  - 0.28 * (model.ph ** 2) + 0.6 * (model.time ** 2) \
#                  - 0.16 * (model.current ** 2)
#     return intercept + linear_coefs + inter_coefs + quad_coefs


def silica_removal_efficiency(model):
    """
    Compute silica removal efficiency function based on coded input variables with
    RSM-provided intercept and linear/interaction/quadratic coefficients
    :param model: pyomo concrete model object
    :return: float
    """
    intercept = 87.44927
    linear_coefs = 0.006637 * model.h_conc + 0.247365 * model.s_conc + 3.38268 * model.ph \
                   - 0.445563 * model.time + 0.126412 * model.current
    inter_coefs = -0.000150 * model.h_conc * model.s_conc - 0.001738 * model.h_conc * model.ph \
                  + 0.000334 * model.h_conc * model.time - 0.000214 * model.h_conc * model.current \
                  + 0.013380 * model.s_conc * model.ph + 0.002172 * model.s_conc * model.time \
                  + 0.017121 * model.s_conc * model.current - 0.031308 * model.ph * model.time \
                  + 0.036911 * model.ph * model.current - 0.005296 * model.time * model.current
    quad_coefs = -0.00000552117 * (model.h_conc ** 2) - 0.004072 * (model.s_conc ** 2) \
                 - 0.070401 * (model.ph ** 2) + 0.002681 * (model.time ** 2) \
                 - 0.031633 * (model.current ** 2)
    return intercept + linear_coefs + inter_coefs + quad_coefs


# def operating_cost(model):
#     """
#     Compute operating cost function based on coded input variables with
#     RSM-provided intercept and linear/interaction/quadratic coefficients
#     :param model: pyomo concrete model object
#     :return: float
#     """
#     intercept = 3.81
#     linear_coefs = 0.12 * model.h_conc - 0.005 * model.s_conc - 0.034 * model.ph \
#                    + 1.3 * model.time + 1.4 * model.current
#     inter_coefs = -0.15 * model.h_conc * model.s_conc - 0.051 * model.h_conc * model.ph \
#                   - 0.27 * model.h_conc * model.time + 0.16 * model.h_conc * model.current \
#                   + 0.12 * model.s_conc * model.ph + 0.17 * model.s_conc * model.time \
#                   + 0.025 * model.s_conc * model.current - 0.094 * model.ph * model.time \
#                   - 0.15 * model.ph * model.current + 0.86 * model.time * model.current
#     quad_coefs = -0.03 * (model.h_conc ** 2) - 0.025 * (model.s_conc ** 2) \
#                  - 0.14 * (model.ph ** 2) + 0.052 * (model.time ** 2) \
#                  - 0.28 * (model.current ** 2)
#     return intercept + linear_coefs + inter_coefs + quad_coefs


def operating_cost(model):
    """
    Compute operating cost function based on coded input variables with
    RSM-provided intercept and linear/interaction/quadratic coefficients
    :param model: pyomo concrete model object
    :return: float
    """
    intercept = 1.60701
    linear_coefs = 0.007692 * model.h_conc - 0.030003 * model.s_conc + 0.839294 * model.ph \
                   - 0.055121 * model.time - 1.70536 * model.current
    inter_coefs = -0.000043 * model.h_conc * model.s_conc - 0.000137 * model.h_conc * model.ph \
                  - 0.000097 * model.h_conc * model.time + 0.000390 * model.h_conc * model.current \
                  + 0.003300 * model.s_conc * model.ph + 0.000596 * model.s_conc * model.time \
                  + 0.000599 * model.s_conc * model.current - 0.003125 * model.ph * model.time \
                  - 0.033989 * model.ph * model.current + 0.025768 * model.time * model.current
    quad_coefs = -0.000000844685 * (model.h_conc ** 2) - 0.000070 * (model.s_conc ** 2) \
                 - 0.035549 * (model.ph ** 2) + 0.000229 * (model.time ** 2) \
                 + 0.057125 * (model.current ** 2)
    return intercept + linear_coefs + inter_coefs + quad_coefs
