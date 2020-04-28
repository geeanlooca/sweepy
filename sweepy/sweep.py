import operator
from copy import deepcopy
from functools import reduce
from itertools import product

import numpy as np
from box import Box


def generate_params(
    config, sweep_params=None, linked_params=None, get_combination=False
):

    if sweep_params is None and linked_params is None:
        yield config
    else:

        def set_param(data, key_list, value):
            partial = reduce(operator.getitem, key_list[:-1], data)
            partial[key_list[-1]] = value

        sweep_params_ = {}
        for k, v in sweep_params.items():

            if not isinstance(v, list):
                v = [v]

            sweep_params_[k] = list(zip(range(len(v)), v))

        keys = sweep_params_.keys()
        values = sweep_params_.values()

        for instance in product(*values):

            config_ = deepcopy(config)

            comb = {k: v[1] for k, v in zip(keys, instance)}

            # Set all the values of the combination in the original params dict
            for k, v in zip(keys, instance):
                value_idx = v[0]
                value = v[1]

                key_list = k.split(".")
                set_param(config_, key_list, value)

                # Check if there are linked parameters for the current key
                if linked_params and k in linked_params:

                    for lk, lv in linked_params[k].items():
                        set_param(config_, lk.split("."), lv[value_idx])

            if get_combination:
                yield config_, comb
            else:
                yield config_



# def sweep(func, params, values, result_fields, linked_params=None):

#     # Check for any linked parameters
#     # A linked parameter is a parameters which assumes a different
#     # value for every value of another swept parameter.
#     # For example, suppose we want to sweep the parameter `foo`
#     # for the values [0, 10, 1000], but another parameter, `bar`
#     # depends on the value of `foo`. We can defined `bar` to be a linked
#     # parameter for `foo`, and assign the values it should obtain when
#     # varying `foo`.

#     pre_shape = []

#     # Compute the first dimensions of the structures
#     # holding the result values
#     for k, v in values.items():
#         pre_shape.append(len(v))

#     values = {k: list(zip(range(len(v)), v)) for k, v in values.items()}
#     combs = []

#     for instance in product(*values.values()):
#         combs.append(dict(zip(values.keys(), instance)))

#     results = []
#     for comb in combs:

#         for k, v, in comb.items():
#             value_index = v[0]
#             parameter_value = v[1]
#             params[k] = parameter_value

#             # Check if current parameter is linked with
#             # other parameters
#             if linked_params and k in linked_params:

#                 # For every linked parameter,
#                 # assign the corresponding value in the
#                 # parameter structure
#                 for lk, lv in linked_params[k].items():
#                     params[lk] = lv[value_index]

#         # Call the function with the current combination of parameters
#         res = func(params)

#         results.append(res)

#     shapes = {}

#     for res in results:
#         for field in result_fields:
#             if field in res:
#                 if field in shapes:
#                     shapes[field].append(res[field].shape)
#                 else:
#                     shapes[field] = [res[field].shape]

#     # Resize to the max shape
#     for field in result_fields:
#         field_shapes = shapes[field]
#         max_shape = field_shapes[0]
#         for shape in field_shapes:
#             try:
#                 max_shape = list(np.maximum(max_shape, shape))
#             except:
#                 max_shape = [int(np.maximum(max_shape, shape))]

#         shapes[field] = max_shape

#     # Initialize the results structure
#     merged_results = Box()
#     for field in result_fields:
#         shape = tuple(pre_shape + shapes[field])
#         merged_results[field] = np.full(shape, np.nan)

#     for comb, res in zip(combs, results):
#         idx = tuple([v[0] for _, v in comb.items()])

#         for field in result_fields:

#             try:
#                 merged_results[field][idx] = res[field]
#             except:

#                 result_shape = res[field].shape

#                 # buld the index array to store the results
#                 # in the first part of the merged results structure
#                 sub_idx = []
#                 for s in result_shape:
#                     sub_idx.append(slice(0, s))

#                 merged_results[field][idx][tuple(sub_idx)] = res[field]

#     return merged_results
