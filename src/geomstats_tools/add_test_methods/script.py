from geomstats_tools.calatrava_utils import (
    keep_only_newly_defined_methods,
    keep_only_public_methods,
    remove_properties,
    remove_repeated_methods,
)
from geomstats_tools.naming_utils import is_test
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

# TODO: in vectorization tests, if empty, assume first argument

# TODO: make keyword arguments be written as keyword arguments


def add_missing_test_methods(config):
    class_ = config.get_class("main")
    test_case_class = config.get_class("test_case")

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
        return False

    code_snippets = {}
    for method_info in methods_info.values():
        code_snippets.update(
            write_test_method_snippets(
                method_info["method"],
                method_info["has_direct_test"],
                method_info["has_vec_test"],
            )
        )

    test_path = test_case_class.module.path
    source_ls = get_source(test_path)

    new_source_ls = add_methods_to_class_given_source(
        source_ls, test_case_class.name, code_snippets
    )

    imports = get_missing_imports(new_source_ls)
    if len(imports) > 0:
        new_source_ls = add_imports_to_source(new_source_ls, imports)

    write_source(test_path, new_source_ls)

    return True
