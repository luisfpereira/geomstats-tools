
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


def add_methods_to_class_given_source(source, class_name, methods_dict):
    start_line, end_line = find_class_lims(class_name, source)
    cls_source = source[start_line:end_line]

    cls_dict = split_class(cls_source)
    cls_dict.update(methods_dict)
    new_cls_source = from_cls_dict_to_list(cls_dict)

    new_source = add_updated_cls_to_source(
        source, new_cls_source, start_line, end_line)

    return new_source
