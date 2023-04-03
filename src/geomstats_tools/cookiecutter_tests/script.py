from geomstats_tools.calatrava_utils import get_cls_module_path

from .utils import (
    get_data_imports,
    get_test_case_imports,
    get_test_imports,
    write_test_case_snippet,
    write_test_data_snippet,
    write_test_snippet,
    write_to_file,
)

# TODO: need to fix import if object exists in current file


def create_test(config):
    class_ = config.get_class("main")

    test_case_cls = config.get_class("test_case")
    data_cls = config.get_class("data")
    test_cls = config.get_class("test")

    if not test_case_cls.found:
        test_case_imports = get_test_case_imports(
            config.packages_config.test_cases_loc.subpackage_import, class_
        )
        test_case_snippet = write_test_case_snippet(class_, test_case_cls.short_name)

        write_to_file(
            get_cls_module_path(test_case_cls),
            test_case_snippet,
            imports=test_case_imports,
        )

    if not data_cls.found:
        data_imports = get_data_imports(
            config.packages_config.data_loc.subpackage_import, class_
        )
        data_snippet = write_test_data_snippet(class_, data_cls.short_name)

        write_to_file(get_cls_module_path(data_cls), data_snippet, imports=data_imports)

    if not test_cls.found:
        test_imports = get_test_imports(
            class_.long_name, test_case_cls.long_name, data_cls.long_name
        )
        test_code_snippet = write_test_snippet(
            class_, test_cls.short_name, test_case_cls.short_name, data_cls.short_name
        )

        write_to_file(
            get_cls_module_path(test_cls), test_code_snippet, imports=test_imports
        )

    return (not test_case_cls.found, not data_cls.found, not test_cls.found)
