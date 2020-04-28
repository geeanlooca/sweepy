import argparse
import os
import sweepy.utils
from sweepy.sweep import generate_params


def is_path(x):
    if os.path.isdir(x):
        return x
    else:
        raise ValueError("Not a path")


def is_file(x):
    if os.path.isfile(x):
        return x
    else:
        raise ValueError("Not a file")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=is_file)
    parser.add_argument("output", type=is_path)
    parser.add_argument("--zero-index", default=False, action="store_true")

    args = parser.parse_args()

    config, filetype = sweepy.utils.load_config(args.input)

    basename = os.path.basename(args.input)
    filename, ext = os.path.splitext(basename)

    # check if the sweep field is defined
    try:
        sweep_params = config["sweep"]["params"]
    except:
        sweep_params = None

    try:
        linked_params = config["sweep"]["linked_params"]
    except:
        linked_params = None

    try:
        del config["sweep"]
    except:
        pass

    config_combinations = list(
        generate_params(config, sweep_params, linked_params, get_combination=True)
    )

    for x, (conf, params) in enumerate(config_combinations):

        idx = x if args.zero_index else x + 1

        if filetype == "yaml":
            conf.to_yaml(os.path.join(args.output, f"{filename}.{idx}{ext}"))
        else:
            conf.to_json(os.path.join(args.output, f"{filename}.{idx}{ext}"))

    # config_bar = tqdm(config_combinations, leave=False)
