from .utils import (
    get_missing_data_methods_names,
    get_test_methods,
)

DEFAULT_MARKERS = ("pytest.mark.vec", "pytest.mark.random")


def print_missing_data_methods(
    config,
    markers=DEFAULT_MARKERS,
):
    test_case_class = config.get_class("test_case")
    data_class = config.get_class("data")

    test_methods = get_test_methods(test_case_class, decorators=markers)
    missing_methods_names = get_missing_data_methods_names(
        test_methods, data_class.methods
    )

    return missing_methods_names
