import os

from geomstats_tools.calatrava_utils import get_class_given_import
from geomstats_tools.parsing_utils import (
    get_source,
    write_source,
)
from geomstats_tools.args_manip import (
    update_geomstats_repo_dir,
    get_info_from_data_import,
)
from .utils import reorder_methods_given_source


# TODO: do this in batch


@update_geomstats_repo_dir
def sort_data_methods(cls_import, *, data_cls_import=None,
                      geomstats_repo_dir=None, tests_loc="tests"):
    data_module_import, data_cls_name = get_info_from_data_import(
        cls_import, data_cls_import, tests_loc
    )

    class_ = get_class_given_import(cls_import, visitor_type="basic-methods")
    method_names = [method.short_name for method in class_.methods
                    if method.short_name.startswith("test_")]

    data_method_names = [f"{name[5:]}_test_data" for name in method_names]

    data_filename = data_module_import.replace(".", os.path.sep) + '.py'
    data_path = os.path.join(geomstats_repo_dir, data_filename)

    data_source = get_source(data_path)
    new_data_source = reorder_methods_given_source(
        data_source, data_cls_name, data_method_names
    )

    write_source(data_path, new_data_source)
