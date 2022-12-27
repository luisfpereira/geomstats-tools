
import os

from geomstats_tools.calatrava_utils import get_classes_given_imports
from geomstats_tools.args_manip import (
    update_test_cls_import,
    update_geomstats_repo_dir,
)

from .utils import (
    keep_only_public_methods,
    remove_repeated_methods,
    collect_info_tests,
    Printer,
)


@update_test_cls_import
@update_geomstats_repo_dir
def print_info_tests(cls_import, *, test_cls_import=None,
                     geomstats_repo_dir=None):
    classes = get_classes_given_imports(
        [cls_import, test_cls_import], visitor_type="basic-methods",
        packages_dir=[os.path.join(geomstats_repo_dir, "geomstats")]
    )

    cls_methods = remove_repeated_methods(
        keep_only_public_methods(classes[0].all_methods)
    )
    cls_methods_names = [method.short_name for method in cls_methods]

    tested_methods = remove_repeated_methods(
        keep_only_public_methods(classes[1].all_methods)
    )
    tested_methods_names = [method.short_name for method in tested_methods
                            if method.short_name.startswith("test_")]

    direct_tests, related_tests, missing_tests = collect_info_tests(
        cls_methods_names, tested_methods_names)

    print(f"`{classes[0].short_name}` with `{classes[1].short_name}`")
    printer = Printer()

    print(
        printer.info_tests_to_str(
            direct_tests, related_tests, missing_tests)
    )
