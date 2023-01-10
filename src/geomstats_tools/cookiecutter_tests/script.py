import os

from geomstats_tools.args_manip import (
    update_geomstats_repo_dir,
    get_info_from_data_import,
    update_test_case_cls_import,
)

from geomstats_tools.calatrava_utils import get_class_given_import
from geomstats_tools.naming_utils import get_test_loc
from .utils import (
    write_test_case_snippet,
    write_test_snippet,
    write_test_data_snippet,
    get_test_case_imports,
    get_test_imports,
    get_data_imports,
    get_path_from_cls_import,
    get_path_from_module_import,
    write_to_file,
)


# TODO: check if file already exists, if yes, check if class already exists

# TODO: probably need to update:
# -get_info_from_data_import

@update_geomstats_repo_dir
def create_test(cls_import, *, test_cls_name=None, test_case_cls_import=None,
                data_cls_import=None,
                geomstats_repo_dir=None, tests_loc="tests"):

    # TODO: need to update test_case_cls_import
    geomstats_dir = os.path.join(geomstats_repo_dir, "geomstats")

    class_ = get_class_given_import(cls_import, packages_dir=[geomstats_dir])

    # TODO: check imports, existence and update file
    # TODO: if exists, then nothing else needs to be done in this section
    # TODO: if file, get_all_classes (and check_class_exists)
    test_case_cls_import = update_test_case_cls_import(class_, test_case_cls_import)
    test_case_cls_name = test_case_cls_import.split('.')[-1]

    test_case_imports = get_test_case_imports(class_)
    test_case_snippet = write_test_case_snippet(class_, test_case_cls_name)

    path = get_path_from_cls_import(test_case_cls_import, geomstats_repo_dir)
    write_to_file(path, test_case_snippet, imports=test_case_imports)

    data_module_import, data_cls_name = get_info_from_data_import(
        test_case_cls_import, data_cls_import, tests_loc
    )
    data_cls_import = f"{data_module_import}.{data_cls_name}"

    data_imports = get_data_imports(tests_loc, class_)
    data_snippet = write_test_data_snippet(class_, data_cls_name)

    path = get_path_from_module_import(data_module_import, geomstats_repo_dir)
    write_to_file(path, data_snippet, imports=data_imports)

    # TODO: out may need to be more informative
    out = test_case_cls_import, data_cls_import

    if class_.is_abstract:
        return out

    test_module_import, test_cls_name_default = get_test_loc(cls_import, tests_loc)
    if test_cls_name is None:
        test_cls_name = test_cls_name_default

    test_imports = get_test_imports(class_.long_name, test_case_cls_import, data_cls_import)
    test_code_snippet = write_test_snippet(class_, test_cls_name,
                                           test_case_cls_name, data_cls_name)

    path = get_path_from_module_import(test_module_import, geomstats_repo_dir)
    write_to_file(path, test_code_snippet, imports=test_imports)

    return out
