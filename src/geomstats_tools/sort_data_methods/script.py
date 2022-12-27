import os

from geomstats_tools.calatrava_utils import get_class_given_import
from geomstats_tools.config_utils import load_from_config
from .utils import (
    get_source,
    get_test_data_loc,
    reorder_methods_given_source,
    write_source,
)


def sort_data_methods(cls_import, data_cls_import=None,
                      geomstats_repo_dir=None, tests_loc="tests"):
    # TODO: add tests_loc to config?
    # TODO: update config style

    if geomstats_repo_dir is None:
        geomstats_repo_dir = load_from_config("geomstats_repo_dir")

    if data_cls_import is None:
        data_module_import, data_cls_name = get_test_data_loc(cls_import, tests_loc)
    else:
        data_cls_import_ls = data_cls_import.split('.')
        data_module_import = '.'.join(data_cls_import_ls[:-1])
        data_cls_name = data_cls_import_ls[-1]

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
