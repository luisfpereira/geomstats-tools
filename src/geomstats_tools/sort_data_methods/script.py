from geomstats_tools.naming_utils import test_name_to_test_data_name
from geomstats_tools.parsing_utils import (
    get_source,
    write_source,
)

from .utils import reorder_methods_given_source

# TODO: do this in batch


def sort_data_methods(config):
    class_ = config.get_class("test_case")

    # TODO: use filter
    method_names = [
        method.short_name
        for method in class_.methods
        if method.short_name.startswith("test_")
    ]

    data_method_names = [test_name_to_test_data_name(name) for name in method_names]

    # TODO: visitor type "basic" suffices. Update `calatrava` to handle this.
    data_class = config.get_class("data")
    data_path = data_class.module.path
    data_cls_name = data_class.name

    data_source = get_source(data_path)
    new_data_source = reorder_methods_given_source(
        data_source, data_cls_name, data_method_names
    )

    write_source(data_path, new_data_source)

    return data_path, data_cls_name
