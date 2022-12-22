
# TODO: move filters to calatrava
# TODO: need to understand how to keep it consistent


def keep_only_public_methods(methods):
    return [method for method in methods
            if method.is_public and not method.is_setter]


def remove_repeated_methods(methods):
    non_rep_methods = []
    for method in methods:
        if method.short_name not in non_rep_methods:
            non_rep_methods.append(method)

    return non_rep_methods


def _get_test_name_default(cls_import):
    cls_import_ls = cls_import.split('.')
    return f"{cls_import_ls[0]}.test.{'.'.join(cls_import_ls[1:])}TestCase"


def has_direct_test(method_name, test_names):
    return f"test_{method_name}" in test_names


def get_related_tests(method_name, test_names):
    related = []
    for test_name in test_names:
        if method_name in test_name:
            related.append(test_name)

    return related


def collect_info_tests(methods_names, test_names):
    test_names = set(test_names)

    direct_tests = []
    related_tests = {}

    missing_tests = []

    for method_name in methods_names:
        has_direct_test_ = has_direct_test(method_name, test_names)

        if has_direct_test_:
            direct_tests.append(method_name)

        related_tests_ = get_related_tests(
            method_name, test_names)
        if related_tests_:
            related_tests[method_name] = related_tests_

        if not has_direct_test_ and len(related_tests_) == 0:
            missing_tests.append(method_name)

    return direct_tests, related_tests, missing_tests


class Printer:

    def __init__(self, tab_spaces=2):
        self.tab_spaces = tab_spaces

    @property
    def _tab(self):
        return " " * self.tab_spaces

    @staticmethod
    def _method_str(method_name):
        return f"\n{method_name}:\n"

    def _direct_method_str(self, has_direct_method):
        return f"{self._tab}has direct test? {has_direct_method}\n"

    def _related_tests_str(self, related_tests):
        string = f"{self._tab}related tests:\n"
        for test_name in related_tests:
            string += f"{self._tab*2}{test_name}\n"

        return string

    def info_tests_to_str(self, direct_tests, related_tests, missing_tests):
        treated = []
        string = ""
        for method_name in direct_tests:
            string += self._method_str(method_name)
            string += self._direct_method_str(True)

            if method_name in related_tests:
                treated.append(method_name)
                string += self._related_tests_str(related_tests[method_name])

        for method_name in related_tests:
            if method_name in treated:
                continue

            string += self._method_str(method_name)
            string += self._direct_method_str(False)
            string += self._related_tests_str(related_tests[method_name])

        if len(missing_tests) == 0:
            return string

        string += "\nmissing tests for:"
        for method_name in missing_tests:
            string += f"\n{self._tab}{method_name}"

        return string
