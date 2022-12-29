

def get_test_cls_import_default(cls_import):
    cls_import_ls = cls_import.split('.')
    return f"{cls_import_ls[0]}.test.{'.'.join(cls_import_ls[1:])}TestCase"


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
