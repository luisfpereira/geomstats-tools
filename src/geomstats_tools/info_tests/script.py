
import os

from geomstats_tools.calatrava_utils import (
    get_class_given_import,
    keep_only_public_methods,
    remove_repeated_methods,
)
from geomstats_tools.args_manip import (
    update_geomstats_repo_dir,
    update_test_case_cls_import,
)
from geomstats_tools.naming_utils import is_test

from .utils import (
    collect_info_tests,
    Printer,
)


@update_geomstats_repo_dir
def print_info_tests(cls_import, *, test_case_cls_import=None,
                     geomstats_repo_dir=None):
    geomstats_dir = os.path.join(geomstats_repo_dir, "geomstats")

    class_ = get_class_given_import(
        cls_import, visitor_type="basic-methods",
        packages_dir=[geomstats_dir]
    )

    test_case_cls_import = update_test_case_cls_import(class_)
    test_case_class = get_class_given_import(
        test_case_cls_import, visitor_type="basic-methods",
        packages_dir=[geomstats_dir]
    )

    cls_methods = remove_repeated_methods(
        keep_only_public_methods(class_.all_methods)
    )
    cls_methods_names = [method.short_name for method in cls_methods]

    tested_methods = remove_repeated_methods(
        keep_only_public_methods(test_case_class.all_methods)
    )
    tested_methods_names = [method.short_name for method in tested_methods
                            if is_test(method.short_name)]

    direct_tests, related_tests, missing_tests = collect_info_tests(
        cls_methods_names, tested_methods_names)

    print(f"`{class_.short_name}` with `{test_case_class.short_name}`")
    printer = Printer()

    print(
        printer.info_tests_to_str(
            direct_tests, related_tests, missing_tests)
    )
