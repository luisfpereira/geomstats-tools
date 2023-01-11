import os

from geomstats_tools.args_manip import (
    update_geomstats_repo_dir,
    update_test_case_cls_import,
)
from geomstats_tools.calatrava_utils import (
    get_class_given_import,
    keep_only_newly_defined_methods,
    keep_only_public_methods,
    remove_properties,
    remove_repeated_methods,
)
from geomstats_tools.naming_utils import (
    get_module_and_cls_from_import,
    is_test,
    module_import_to_filename,
)
from geomstats_tools.parsing_utils import (
    add_imports_to_source,
    add_methods_to_class_given_source,
    get_source,
    write_source,
)

from .utils import (
    collect_methods_info,
    get_missing_imports,
    write_test_method_snippets,
)


@update_geomstats_repo_dir
def add_missing_test_methods(
    cls_import, *, test_case_cls_import=None, geomstats_repo_dir=None
):

    # TODO: syntax sugar?
    geomstats_dir = os.path.join(geomstats_repo_dir, "geomstats")

    class_ = get_class_given_import(
        cls_import, visitor_type="basic-methods", packages_dir=[geomstats_dir]
    )

    test_case_cls_import = update_test_case_cls_import(class_, test_case_cls_import)
    test_case_class = get_class_given_import(
        test_case_cls_import, visitor_type="basic-methods", packages_dir=[geomstats_dir]
    )

    cls_methods = keep_only_newly_defined_methods(
        remove_properties(
            remove_repeated_methods(keep_only_public_methods(class_.methods)),
        ),
        class_.base_methods,
    )

    tested_methods = remove_repeated_methods(
        keep_only_public_methods(test_case_class.all_methods)
    )
    tested_methods_names = [
        method.short_name for method in tested_methods if is_test(method.short_name)
    ]

    methods_info = collect_methods_info(cls_methods, tested_methods_names)
    if len(methods_info) == 0:
        return

    code_snippets = {}
    for method_info in methods_info.values():
        code_snippets.update(
            write_test_method_snippets(
                method_info["method"],
                method_info["has_direct_test"],
                method_info["has_vec_test"],
            )
        )

    # TODO: sintax sugar?
    test_module_import, test_cls_name = get_module_and_cls_from_import(
        test_case_cls_import
    )
    test_filename = module_import_to_filename(test_module_import)
    test_path = os.path.join(geomstats_repo_dir, test_filename)
    source_ls = get_source(test_path)

    new_source_ls = add_methods_to_class_given_source(
        source_ls, test_cls_name, code_snippets
    )

    imports = get_missing_imports(new_source_ls)
    if len(imports) > 0:
        new_source_ls = add_imports_to_source(new_source_ls, imports)

    write_source(test_path, new_source_ls)

    return test_path, test_case_cls_import, test_cls_name
