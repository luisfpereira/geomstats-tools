
import os

from geomstats_tools.naming_utils import (
    get_test_case_cls_import_from_class,
    get_test_data_cls_import_from_class,
    cls_import_to_filename,
    module_import_to_filename,
)
from geomstats_tools.parsing_utils import add_imports_to_source
from geomstats_tools.str_utils import VERIFICATION_MSG, TAB


def _from_class_to_test_case_name(class_):
    return f"{class_.short_name.replace(' ', '')}TestCase"


def _from_class_to_base_test_cases_names(class_):
    return [_from_class_to_test_case_name(base_class) for base_class in class_.bases]


def _from_class_to_test_data_name(class_):
    return f"{class_.short_name.replace(' ', '')}TestData"


def _from_class_to_base_test_data_names(class_):
    return [_from_class_to_test_data_name(base_class) for base_class in class_.bases]


def get_test_case_imports(class_):
    return [get_test_case_cls_import_from_class(base) for base in class_.bases]


def write_test_case_snippet(class_, class_test_case, level=0):
    cls_lvl = level + 1

    base_classes_test_cases = ', '.join(_from_class_to_base_test_cases_names(class_))

    code = f"{TAB * level}class {class_test_case}({base_classes_test_cases}):\n"
    code += f"{TAB*cls_lvl}pass\n"

    return code


def get_test_imports(class_cls_import, test_case_cls_import, data_cls_import,
                     parametrizer="DataBasedParametrizer"):
    imports = [
        "random",
        "pytest",
        class_cls_import,
        test_case_cls_import,
        f"geomstats.test.parametrizers.{parametrizer}",
        data_cls_import,
    ]

    return imports


def _write_fixture_example(class_name, fixture_name="spaces", level=0):
    fnc_lvl = level + 1
    params_lvl = fnc_lvl + 1

    code = (
        f"{TAB*level}@pytest.fixture(\n"
        f'{TAB*(fnc_lvl)}scope="class",\n'
        f"{TAB*(fnc_lvl)}params=[\n"
        f"{TAB*params_lvl}2,\n"
        f"{TAB*params_lvl}random.randint(3, 5),\n"
        f"{TAB*fnc_lvl}],\n"
        f"{TAB*level})\n"
        f"{TAB*level}def {fixture_name}(request):\n"
        f"{TAB*fnc_lvl}{VERIFICATION_MSG}\n"
        f"{TAB*fnc_lvl}request.cls.space = {class_name}(request.param)\n\n\n"
    )

    return code


def _write_test_snippet(fixture_name, test_cls_name, test_case_cls_name,
                        data_cls_name,
                        parametrizer="DataBasedParametrizer", level=0):
    cls_lvl = level + 1

    code = (
        f'{TAB*level}@pytest.mark.usefixtures("{fixture_name}")\n'
        f"{TAB*level}class {test_cls_name}({test_case_cls_name}, metaclass={parametrizer}):\n"
        f"{TAB*cls_lvl}testing_data = {data_cls_name}()\n\n"
    )
    return code


def write_test_snippet(class_, test_cls_name, test_case_cls_name, data_cls_name):
    fixture_name = "spaces"
    code = _write_fixture_example(class_.short_name, fixture_name)
    code += _write_test_snippet(fixture_name, test_cls_name, test_case_cls_name,
                                data_cls_name)

    return code


def get_data_imports(tests_loc, class_):
    return [get_test_data_cls_import_from_class(tests_loc, base) for base in class_.bases]


def write_test_data_snippet(class_, data_cls_name, level=0):
    cls_lvl = level + 1

    base_classes_test_data = ', '.join(_from_class_to_base_test_data_names(class_))

    code = (
        f"{TAB*level}class {data_cls_name}({base_classes_test_data}):\n"
        f"{TAB*cls_lvl}pass\n\n"

    )

    return code


def get_path_from_cls_import(cls_import, repo_dir):
    return os.path.join(
        repo_dir,
        cls_import_to_filename(cls_import),
    )


def get_path_from_module_import(module_import, repo_dir):
    return os.path.join(
        repo_dir,
        module_import_to_filename(module_import)
    )


def _write_to_file(path, source_ls):
    with open(path, 'w') as file:
        file.writelines(source_ls)


def write_to_file(path, code_snippet, imports=()):
    # TODO: imports may need to be used in other tools
    if os.path.exists(path):
        code_snippet = f"\n\n{code_snippet}"

        with open(path, 'r') as file:
            source_ls = file.readlines()
    else:
        source_ls = []

    source_ls.extend(code_snippet.splitlines(True))

    if not imports:
        _write_to_file(path, source_ls)
        return

    new_source_ls = add_imports_to_source(source_ls, imports)
    _write_to_file(path, new_source_ls)
