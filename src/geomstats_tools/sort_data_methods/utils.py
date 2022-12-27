
def get_source(path):
    with open(path, 'r') as file:
        source = file.readlines()
    return source


def write_source(path, source):
    with open(path, 'w') as file:
        file.writelines(source)


def find_class_lims(class_name, source):
    start_line = None
    end_line = None

    to_break = False
    for i, line in enumerate(source):
        if line.startswith(f"class {class_name}"):
            start_line = i
            to_break = True
            continue

        if to_break and not line.strip() == "" and not line.startswith(' '):
            end_line = i
            break

    else:
        if start_line is None:
            raise Exception("Cannot find class")

        end_line = i

    return start_line, end_line


def _is_function_def_start(line, indentation):
    if line.startswith(f"{indentation}def") or line.startswith(f"{indentation}@"):
        return True

    return False


def _get_function_name_from_def(line):
    line = line.strip()
    return line[4:line.index("(")]


def split_class(class_source):
    # naive split using def

    header = []
    line = ""
    i = 0
    while True:
        # TODO: class with no methods
        line = class_source[i]
        stripped_line = line.strip()
        if stripped_line.startswith("def") or stripped_line.startswith("@"):
            indentation = " " * line.index("d")
            break

        header.append(line)
        i += 1

    class_ = {"header": header}

    cls_name = ""
    cls_lines = []
    for line in class_source[i:]:
        if _is_function_def_start(line, indentation) and cls_name:
            if cls_lines:
                class_[cls_name] = cls_lines

            cls_name = ""
            cls_lines = []

        if line.startswith(f"{indentation}def"):
            cls_name = _get_function_name_from_def(line)

        cls_lines.append(line)

    if cls_lines:
        class_[cls_name] = cls_lines

    return class_


def reorder_methods(cls_dict, order):
    # methods not in order are placed first
    cls_dict_ = {}
    to_order_dict = {}
    for key, value in cls_dict.items():
        if key in order:
            to_order_dict[key] = value
        else:
            cls_dict_[key] = value

    sorted_dict = {}
    for key in order:
        if key in to_order_dict:
            sorted_dict[key] = to_order_dict[key]

    cls_dict_.update(sorted_dict)
    return cls_dict_


def from_cls_dict_to_list(cls_dict):
    lines = []
    for lines_ in cls_dict.values():
        if lines and lines[-1] != "\n":
            lines_.append('\n')
        lines.extend(lines_)

    return lines


def add_updated_cls_to_source(source, cls_source, start_line, end_line):
    source_ = [line for line in source[:start_line]]
    for line in cls_source:
        source_.append(line)

    for line in source[end_line:]:
        source_.append(line)

    source.append('\n')
    return source_


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


def reorder_methods_given_source(source, class_name, methods_order):

    start_line, end_line = find_class_lims(class_name, source)
    cls_source = source[start_line:end_line]

    cls_dict = split_class(cls_source)
    cls_ordered_dict = reorder_methods(cls_dict, methods_order)
    ordered_cls_source = from_cls_dict_to_list(cls_ordered_dict)

    new_source = add_updated_cls_to_source(
        source, ordered_cls_source, start_line, end_line)

    return new_source


def collect_methods_with_given_decorators(methods, decorators):
    decorators_set = set(decorators)
    return [method for method in methods if decorators_set.intersection(method.decorator_list)]
