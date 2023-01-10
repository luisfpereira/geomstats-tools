
import os

from geomstats_tools.args_manip import (
    get_info_from_data_import,
    update_geomstats_repo_dir
)
from geomstats_tools.calatrava_utils import get_classes_given_imports

from .utils import (
    get_missing_data_methods_names,
    get_test_methods
)

DEFAULT_MARKERS = ('pytest.mark.vec', 'pytest.mark.random')


@update_geomstats_repo_dir
def print_missing_data_methods(test_cls_import, *, data_cls_import=None,
                               geomstats_repo_dir=None, tests_loc="tests",
                               markers=DEFAULT_MARKERS):
    data_module_import, data_cls_name = get_info_from_data_import(
        test_cls_import, data_cls_import, tests_loc
    )

    data_cls_import = f"{data_module_import}.{data_cls_name}"

    packages_dir = [os.path.join(geomstats_repo_dir, "geomstats"),
                    os.path.join(geomstats_repo_dir, tests_loc)]
    class_, data_class = get_classes_given_imports(
        [test_cls_import, data_cls_import], visitor_type="basic-methods",
        packages_dir=packages_dir
    )

    test_methods = get_test_methods(class_, decorators=markers)
    missing_methods_names = get_missing_data_methods_names(
        test_methods, data_class.methods)

    return missing_methods_names
