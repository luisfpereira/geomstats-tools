from geomstats_tools.naming_utils import (
    is_test,
    test_name_to_test_data_name,
)


def collect_methods_with_given_decorators(methods, decorators):
    decorators_set = set(decorators)
    return [
        method
        for method in methods
        if decorators_set.intersection(method.decorator_list)
    ]


def get_test_methods(class_, decorators=None):
    if decorators is None:
        class_methods = class_.methods
    else:
        class_methods = collect_methods_with_given_decorators(
            class_.methods, decorators=decorators
        )

    return [method for method in class_methods if is_test(method.short_name)]


def get_missing_data_methods_names(test_methods, data_methods):

    test_methods_names = [
        method.short_name for method in test_methods if is_test(method.short_name)
    ]
    required_data_methods_names = [
        test_name_to_test_data_name(name) for name in test_methods_names
    ]

    data_methods_names = {method.short_name for method in data_methods}
    missing_methods_names = []
    for method_name in required_data_methods_names:
        if method_name in data_methods_names:
            continue

        missing_methods_names.append(method_name)

    return missing_methods_names
