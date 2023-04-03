from geomstats_tools.calatrava_utils import (
    keep_only_public_methods,
    remove_repeated_methods,
)
from geomstats_tools.naming_utils import is_test

from .utils import (
    Printer,
    collect_info_tests,
)

# TODO: some methods are printed twice

# TODO: receive a logger instead of printer?


def print_info_tests(config):
    class_ = config.get_class("main")
    test_case_class = config.get_class("test_case")

    # TODO: use filters
    cls_methods = remove_repeated_methods(keep_only_public_methods(class_.all_methods))
    cls_methods_names = [method.short_name for method in cls_methods]

    tested_methods = remove_repeated_methods(
        keep_only_public_methods(test_case_class.all_methods)
    )
    tested_methods_names = [
        method.short_name for method in tested_methods if is_test(method.short_name)
    ]

    direct_tests, related_tests, missing_tests = collect_info_tests(
        cls_methods_names, tested_methods_names
    )

    print(f"`{class_.short_name}` with `{test_case_class.short_name}`")
    printer = Printer()

    print(printer.info_tests_to_str(direct_tests, related_tests, missing_tests))
