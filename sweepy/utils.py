import json
import re

import yaml
from box import Box

loader = yaml.SafeLoader
loader.add_implicit_resolver(
    "tag:yaml.org,2002:float",
    re.compile(
        """^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$""",
        re.X,
    ),
    list("-+0123456789."),
)


def load_config(filename):

    with open(filename, "r") as f:

        content = f.read()

        try:
            json_content = json.loads(content)
            return Box(json_content), "json"
        except ValueError:
            pass
        return Box.from_yaml(content), "yaml"
