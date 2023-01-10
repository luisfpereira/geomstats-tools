import os


def get_test_case_cls_import(cls_import, is_abstract=False):
    cls_import_ls = cls_import.split('.')

    import_ = f"{cls_import_ls[0]}.test."
    if is_abstract:
        import_ += f"{'.'.join(cls_import_ls[1:-2])}.base.{cls_import_ls[-1]}"
    else:
        import_ += ".".join(cls_import_ls[1:])

    import_ += "TestCase"
    return import_


def get_test_case_cls_import_from_class(class_):
    return get_test_case_cls_import(class_.long_name, class_.is_abstract)


def get_test_data_cls_import(tests_loc, cls_import, is_abstract=False):
    cls_import_ls = cls_import.split('.')

    import_ = f"{tests_loc}.data."
    if is_abstract:
        import_ += "base"
    else:
        import_ += f"{cls_import[-2]}"

    import_ += f"_data.{cls_import_ls[-1]}TestData"
    return import_


def get_test_data_cls_import_from_class(tests_loc, class_):
    return get_test_data_cls_import(tests_loc, class_.long_name, class_.is_abstract)


def get_data_cls_name(cls_name):
    if cls_name.startswith("Test"):
        start = cls_name[4:]

    else:
        start = cls_name.replace("TestCase", "")

    return f"{start}TestData"


def get_test_data_loc(cls_import, tests_loc):
    cls_import_ls = cls_import.split('.')

    cls_name = cls_import_ls[-1]
    module_name = cls_import_ls[-2]

    data_cls_name = get_data_cls_name(cls_name)

    return f"{tests_loc}.data.{module_name}_data", data_cls_name


def get_test_cls_name(cls_name):
    # TODO: may need to handle differently private cases
    return f"Test{cls_name.replace(' ', '')}"


def get_test_loc(cls_import, tests_loc):
    cls_import_ls = cls_import.split('.')

    cls_name = cls_import_ls[-1]
    module_name = cls_import_ls[-2]

    test_cls_name = get_test_cls_name(cls_name)

    return f"{tests_loc}.tests_geomstats.test_{module_name}", test_cls_name


def get_module_and_cls_from_import(cls_import):
    data_cls_import_ls = cls_import.split('.')
    module_import = '.'.join(data_cls_import_ls[:-1])
    cls_name = data_cls_import_ls[-1]

    return module_import, cls_name


def is_test(method_name):
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
    cls_import_ls = cls_import.split('.')
    return f"{os.path.sep}".join(cls_import_ls[:-1]) + '.py'


def module_import_to_filename(module_import):
    return module_import.replace('.', os.path.sep) + ".py"
