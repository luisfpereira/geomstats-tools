

from geomstats_tools.calatrava_utils import collect_imports
from geomstats_tools.str_utils import TAB

# TODO: improve argument name for distinction between source and source_ls
# TODO: solve with decorator?


def get_source(path):
    with open(path, 'r') as file:
        source = file.readlines()
    return source


def write_source(path, source_ls):
    with open(path, 'w') as file:
        file.writelines(source_ls)


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

        end_line = i + 1

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
    while i < len(class_source):
        line = class_source[i]
        stripped_line = line.strip()
        if stripped_line.startswith("def") or stripped_line.startswith("@"):
            indentation = " " * line.index("d")
            break

        header.append(line)
        i += 1

    class_ = {"header": header}
    if i == len(class_source):
        if class_["header"][-1].strip() == "pass":
            class_["header"] = class_["header"][:-1]

        return class_

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


def from_cls_dict_to_list(cls_dict):
    lines = []
    for lines_ in cls_dict.values():
        if type(lines_) is str:
            lines_ = lines_.splitlines(True)

        if lines and lines[-1] != "\n":
            lines_.append('\n')
        lines.extend(lines_)

    return lines


def add_updated_cls_to_source(source, cls_source, start_line, end_line):
    if type(cls_source) is str:
        cls_source = cls_source.splitlines(True)

    source_ = source[:start_line]
    source_.extend(cls_source)
    source_.extend(source[end_line:])

    source.append('\n')
    return source_


def add_methods_to_class_given_source(source_ls, class_name, methods_dict):
    start_line, end_line = find_class_lims(class_name, source_ls)
    cls_source = source_ls[start_line:end_line]

    cls_dict = split_class(cls_source)
    cls_dict.update(methods_dict)
    new_cls_source = from_cls_dict_to_list(cls_dict)

    new_source_ls = add_updated_cls_to_source(
        source_ls, new_cls_source, start_line, end_line)

    return new_source_ls


def find_last_import_line(source_ls):
    last_line = 0
    for line_num, line in enumerate(source_ls):
        if any(line.startswith(str_) for str_ in [
            "from", "import", ")",
        ]):
            last_line = line_num
        elif not any(line.startswith(str_) for str_ in [
            "\n", "#", '"', "'",
        ]):
            break

    return last_line


def _manipulate_imports(imports_ls):
    # TODO: import pytest and pytest.something case is not captured
    imports_ = []
    for import_ in imports_ls:
        import_ls = import_.split('.')
        if len(import_ls) == 1:
            imports_.append((import_ls[0], None))
        else:
            imports_.append((".".join(import_ls[:-1]), import_ls[-1]))

    imports_dict = {}
    for import_ in imports_:
        if import_[0] not in imports_dict:
            imports_dict[import_[0]] = []

        if import_[1] is not None:
            imports_dict[import_[0]].append(import_[1])

    return imports_dict


def _write_imports_snippet_ls(imports_ls):
    imports_dict = _manipulate_imports(imports_ls)

    code = []
    for key, values in imports_dict.items():
        if len(values) == 0:
            code.append(f"import {key}\n")

        elif len(values) == 1:
            code.append(f"from {key} import {values[0]}\n")

        else:
            code.append(f"from {key} import (\n")
            for value in values:
                code.append(f"{TAB}{value},\n")
            code.append(')\n')

    return code


def add_imports_to_source(source_ls, imports):
    # TODO: maybe use isort here?

    existing_imports = collect_imports('\n'.join(source_ls))

    imports_to_add = [import_ for import_ in imports
                      if import_ not in existing_imports]

    if len(imports_to_add) == 0:
        return source_ls

    code_ls = _write_imports_snippet_ls(imports_to_add)

    last_import_line = find_last_import_line(source_ls)
    new_source_ls = source_ls[:last_import_line + 1]
    new_source_ls.append("\n")
    new_source_ls.extend(code_ls)
    new_source_ls.extend(source_ls[last_import_line + 1:])

    return new_source_ls
