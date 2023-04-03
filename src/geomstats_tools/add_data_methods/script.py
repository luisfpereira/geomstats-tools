from geomstats_tools.missing_data_methods.utils import (
    get_missing_data_methods_names,
    get_test_methods,
)
from geomstats_tools.parsing_utils import (
    add_methods_to_class_given_source,
    get_source,
    write_source,
)

from .utils import (
    identify_test_type,
    write_test_data_snippet,
)

DEFAULT_MARKERS = ("pytest.mark.vec", "pytest.mark.random")


# TODO: need to check if data exists in parent

# TODO: add data for `pytest.mark.shape`


def add_missing_data_methods(config, markers=DEFAULT_MARKERS):
    test_case = config.get_class("test_case")
    data_class = config.get_class("data")

    test_methods = get_test_methods(test_case, decorators=markers)
    missing_methods_names = get_missing_data_methods_names(
        test_methods, data_class.methods
    )

    if len(missing_methods_names) == 0:
        return False

    data_method_to_test_type = identify_test_type(
        test_methods, missing_methods_names, markers
    )

    methods_snippets = {
        func_name: [write_test_data_snippet(func_name, type_)]
        for func_name, type_ in data_method_to_test_type.items()
    }

    module_path = data_class.module.path
    data_source = get_source(module_path)

    new_data_source = add_methods_to_class_given_source(
        data_source, data_class.name, methods_snippets
    )

    write_source(module_path, new_data_source)

    return True
