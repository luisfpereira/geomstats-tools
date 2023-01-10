import functools

from geomstats_tools.config_utils import load_from_config
from geomstats_tools.naming_utils import (
    get_module_and_cls_from_import,
    get_test_case_cls_import_from_class,
    get_test_data_loc,
)


def update_geomstats_repo_dir(func):
    @functools.wraps(func)
    def _wrapped(*args, geomstats_repo_dir=None, **kwargs):
        if geomstats_repo_dir is None:
            geomstats_repo_dir = load_from_config("geomstats_repo_dir")

        return func(*args, geomstats_repo_dir=geomstats_repo_dir, **kwargs)

    return _wrapped


def update_test_case_cls_import(class_, test_cls_import=None):
    if test_cls_import is not None:
        return test_cls_import

    return get_test_case_cls_import_from_class(class_)


def get_info_from_data_import(cls_import, data_cls_import, tests_loc):
    # TODO: add tests_loc to config?
    # TODO: update config style

    if data_cls_import is None:
        data_module_import, data_cls_name = get_test_data_loc(cls_import, tests_loc)
    else:
        data_module_import, data_cls_name = get_module_and_cls_from_import(
            data_cls_import
        )

    return data_module_import, data_cls_name
