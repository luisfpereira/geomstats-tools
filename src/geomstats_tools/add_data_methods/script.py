import os

from geomstats_tools.args_manip import (
    get_info_from_data_import,
    update_geomstats_repo_dir,
)
from geomstats_tools.calatrava_utils import get_classes_given_imports
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


@update_geomstats_repo_dir
def add_missing_data_methods(
    test_cls_import,
    *,
    data_cls_import=None,
    geomstats_repo_dir=None,
    tests_loc="tests",
    markers=DEFAULT_MARKERS,
):
    data_module_import, data_cls_name = get_info_from_data_import(
        test_cls_import, data_cls_import, tests_loc
    )

    data_cls_import = f"{data_module_import}.{data_cls_name}"

    packages_dir = [
        os.path.join(geomstats_repo_dir, "geomstats"),
        os.path.join(geomstats_repo_dir, tests_loc),
    ]
    class_, data_class = get_classes_given_imports(
        [test_cls_import, data_cls_import],
        visitor_type="basic-methods",
        packages_dir=packages_dir,
    )

    test_methods = get_test_methods(class_, decorators=markers)
    missing_methods_names = get_missing_data_methods_names(
        test_methods, data_class.methods
    )

    if len(missing_methods_names) == 0:
        return

    data_method_to_test_type = identify_test_type(
        test_methods, missing_methods_names, markers
    )

    methods_snippets = {
        func_name: [write_test_data_snippet(func_name, type_)]
        for func_name, type_ in data_method_to_test_type.items()
    }

    data_filename = data_module_import.replace(".", os.path.sep) + ".py"
    data_path = os.path.join(geomstats_repo_dir, data_filename)
    data_source = get_source(data_path)

    new_data_source = add_methods_to_class_given_source(
        data_source, data_cls_name, methods_snippets
    )

    write_source(data_path, new_data_source)

    return data_path, data_cls_name
