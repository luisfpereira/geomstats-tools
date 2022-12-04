
import os

from calatrava.parser.ast.uml import (
    PackageManager,
    Package,
)


def get_base_class_names(cls_import):
    visitor_type = "basic"
    package = Package("geomstats", classes_visitor=visitor_type)
    package_manager = PackageManager([package])

    package_manager.find(cls_import)
    package_manager.update_inheritance()

    class_ = package_manager.get_classes()[cls_import]
    if not class_.found:
        raise Exception(f"Cannot find `{cls_import}`")
    return [base_class.name for base_class in class_.bases]


def get_placeholders(cls_import, base_names):
    placeholders = {
        "class_name": cls_import.split(".")[-1],
        "class_full_import": ".".join(cls_import.split(".")[:-1]),
        "class_test_import": "geomstats.test." + ".".join(cls_import.split(".")[1:-1]),
        "class_short_filename": cls_import.split(".")[-2],
        "base_classes_test_cases": ", ".join([f"{base_name}TestCase" for base_name in base_names]),
        "base_classes_test_data": ", ".join([f"{base_name}TestData" for base_name in base_names]),
    }

    return placeholders


def read_file(template_dir, short_filename):
    filename = os.path.join(template_dir, short_filename)
    with open(filename, "r") as file:
        code_str = file.read()

    return code_str


def update_code_str(code_str, placeholders):
    for placeholder_name, value in placeholders.items():
        code_str = code_str.replace(f"`{placeholder_name}`", value)

    return code_str


def get_updated_code(placeholders, short_filename, template_dir):
    code_str = read_file(template_dir, short_filename)
    return update_code_str(code_str, placeholders)


def update_filename(class_short_filename, short_filename):
    return short_filename.replace("class_short_filename", class_short_filename)


def get_updated_codes(placeholders, short_filenames, template_dir):
    codes = {}
    for short_filename in short_filenames:
        code_str = get_updated_code(placeholders, short_filename, template_dir)

        new_filename = update_filename(placeholders["class_short_filename"], short_filename)
        codes[new_filename] = code_str

    return codes


def output_to_file(path, code):
    if os.path.exists(path):
        code = f"\n\n{code}"

    with open(path, 'a') as file:
        file.write(code)


def _map_file_to_dir(filename, cls_import):
    tests_dir = "tests2"
    if filename.startswith("test_"):
        return os.path.join(tests_dir, "tests_geomstats", filename)

    if filename.endswith("_data.py"):
        return os.path.join(tests_dir, "data", filename)

    init_path = f"geomstats{os.path.sep}test{os.path.sep}" + f"{os.path.sep}".join(cls_import.split('.')[1:-2])
    return os.path.join(init_path, filename)


def output_to_files(codes, geomstats_repo_dir, cls_import):
    paths_to_log = []
    for filename, code in codes.items():
        path_in_repo = _map_file_to_dir(filename, cls_import)
        path = os.path.join(geomstats_repo_dir, path_in_repo)

        paths_to_log.append(path_in_repo)

        output_to_file(path, code)

    msg = "Created or updated:"
    for path in paths_to_log:
        msg += f"\n\t-{path}"

    print(msg)


if __name__ == "__main__":
    template_dir = "template"
    geomstats_repo_dir = "/user/lgomespe/home/Repos/github/geomstats"
    cls_import = "geomstats.geometry.euclidean.Euclidean"

    base_names = get_base_class_names(cls_import)
    placeholders = get_placeholders(cls_import, base_names)

    filenames = [
        "test_class_short_filename.py",
        "class_short_filename.py",
        "class_short_filename_data.py"
    ]

    codes = get_updated_codes(placeholders, filenames, template_dir)

    output_to_files(codes, geomstats_repo_dir, cls_import)
