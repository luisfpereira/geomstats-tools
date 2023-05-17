import os


def is_metric(class_):
    for cmp_name in ["Connection", "Metric"]:
        if cmp_name in class_.long_name:
            break
    else:
        return False

    return True


def get_test_case_cls_import(test_cases_subpackage_import, class_):
    cls_import = class_.long_name

    cls_import_ls = cls_import.split(".")

    import_ = f"{test_cases_subpackage_import}."
    import_ += ".".join(cls_import_ls[1:-1])

    cls_name = cls_import_ls[-1]
    if cls_name.startswith("_"):
        cls_name = cls_name[1:]

    import_ += f".{cls_name}TestCase"
    return import_


def get_test_default_cls_name(cls_name):
    # TODO: may need to handle differently private cases
    return f"Test{cls_name.replace(' ', '')}"


def get_test_cls_import(tests_subpackage_import, class_, test_cls_name=None):
    cls_import = class_.long_name

    cls_import_ls = cls_import.split(".")

    cls_name = cls_import_ls[-1]
    subpackage_name = ".test_".join(cls_import_ls[1:-1])

    if test_cls_name is None:
        test_cls_name = get_test_default_cls_name(cls_name)

    return f"{tests_subpackage_import}.test_{subpackage_name}.{test_cls_name}"


def is_test_case_cls(class_name):
    return class_name.endswith("TestCase")


def get_data_cls_import_from_class(data_module_import, class_):
    # TODO: simplify
    return get_data_cls_import(data_module_import, class_.long_name, class_.is_abstract)


def get_data_cls_name(cls_name):
    if cls_name.startswith("Test"):
        start = cls_name[4:]

    else:
        start = cls_name.replace("TestCase", "")

    return f"{start}TestData"


def get_data_cls_import(data_module_import, cls_import, is_abstract=False):
    """Get test data class import.

    Parameters
    ----------
    data_module_import : str
        Import of data module.
    cls_import : str
        Can be the class or the test case import.
    is_abstract: bool
        Used only if cls_import is the class import .
    """
    cls_import_ls = cls_import.split(".")

    cls_name = cls_import_ls[-1]
    index = 2 if is_test_case_cls(cls_name) else 1

    subpackage_name = "test_"
    subpackage_name += ".test_".join(cls_import_ls[index:-2])

    module_name = cls_import_ls[-2]

    data_cls_name = get_data_cls_name(cls_name)

    return f"{data_module_import}.{subpackage_name}.data.{module_name}.{data_cls_name}"


def is_test(method_name):
    # TODO: is_test_method instead?
    return method_name.startswith("test_")


def is_test_data(method_name):
    return method_name.endswith("_test_data")


def test_name_to_test_data_name(test_name):
    return test_name[5:] + "_test_data"


def test_data_name_to_test_name(data_name):
    return f"test_{data_name[:-10]}"


def has_direct_test(method_name, test_names):
    return f"test_{method_name}" in test_names


def has_vec_test(method_name, tests_names):
    return f"test_{method_name}_vec" in tests_names


def cls_import_to_filename(cls_import):
    cls_import_ls = cls_import.split(".")
    return f"{os.path.sep}".join(cls_import_ls[:-1]) + ".py"


def module_import_to_filename(module_import):
    return module_import.replace(".", os.path.sep) + ".py"
