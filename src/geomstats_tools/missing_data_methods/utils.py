def collect_methods_with_given_decorators(methods, decorators):
    decorators_set = set(decorators)
    return [method for method in methods if decorators_set.intersection(method.decorator_list)]


def get_missing_data_methods_names(class_, data_class, decorators=None):
    if decorators is None:
        class_methods = class_.methods
    else:
        class_methods = collect_methods_with_given_decorators(
            class_.methods,
            decorators=decorators)

    # TODO: create methods for conversion of methods names (use geomstats?)
    test_methods_names = [method.short_name for method in class_methods
                          if method.short_name.startswith("test_")]
    required_data_methods_names = [f"{name[5:]}_test_data" for name in test_methods_names]

    data_methods_names = set([method.short_name for method in data_class.methods])

    missing_methods_names = []
    for method_name in required_data_methods_names:
        if method_name in data_methods_names:
            continue

        missing_methods_names.append(method_name)

    return missing_methods_names
