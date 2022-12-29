from geomstats_tools.naming_utils import test_data_name_to_test_name


def identify_test_type(test_methods, missing_data_methods_names, markers):
    test_methods_by_name = {method.short_name: method for method in test_methods}
    data_method_to_test_type = {}
    markers_set = set(markers)
    for data_method_name in missing_data_methods_names:
        method = test_methods_by_name[
            test_data_name_to_test_name(data_method_name)
        ]
        markers_intersect = markers_set.intersection(method.decorator_list)
        if markers_intersect:
            marker, = markers_intersect
            data_method_to_test_type[data_method_name] = marker.split('.')[-1]

    return data_method_to_test_type


TYPE2SNIPPET = {
    "vec": """    def {func_name}(self):
        data = [dict(n_reps=n_reps) for n_reps in self.N_VEC_REPS]
        return self.generate_tests(data)\n""",
    "random": """    def {func_name}(self):
        data = [dict(n_points=n_points) for n_points in self.N_RANDOM_POINTS]
        return self.generate_tests(data)\n""",
}


def write_test_data_snippet(func_name, type_):
    snippet = TYPE2SNIPPET[type_]
    return snippet.format(func_name=func_name)
