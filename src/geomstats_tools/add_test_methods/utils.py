from geomstats_tools.naming_utils import (
    has_direct_test,
    has_vec_test,
)
from geomstats_tools.str_utils import (
    TAB,
    VERIFICATION_MSG,
)

IGNORES = ("default_metric",)


def collect_methods_info(cls_methods, tested_methods_names):
    tested_methods_names = set(tested_methods_names)

    methods_info = {}
    for method in cls_methods:
        if method.short_name in IGNORES:
            continue

        if "random" in method.short_name:
            continue

        has_direct_test_ = has_direct_test(method.short_name, tested_methods_names)
        has_vec_test_ = has_vec_test(method.short_name, tested_methods_names)

        if not (has_direct_test_ and has_vec_test_):
            # TODO: use named tuple instead?
            methods_info[method.short_name] = {
                "method": method,
                "has_direct_test": has_direct_test_,
                "has_vec_test": has_vec_test_,
            }

    return methods_info


def _write_direct_test_snippet(method, level=1):
    args = [arg for arg in method.args_list if arg != "self"]
    fnc_lvl = level + 1

    code = TAB * level + "def test_{func_name}(self, {args_list}, expected, atol):\n"
    code += f"{TAB*fnc_lvl}{VERIFICATION_MSG}\n"

    code += TAB * fnc_lvl + "res = self.space.{func_name}({args_list})\n"
    code += f"{TAB*fnc_lvl}self.assertAllClose(res, expected, atol=atol)\n"

    return code.format(func_name=method.short_name, args_list=", ".join(args))


def _base_point_snippet(arg_name, level=2):
    return f"{TAB*level}{arg_name} = self.space.random_point()\n"


def _tangent_point_snippet(arg_name, base_point="base_point", level=2):
    return f"{TAB*level}{arg_name} = get_random_tangent_vec(self.space, {base_point})\n"


def _write_point_creation_snippet(args, level=2):
    code = ""

    point_args = [arg for arg in args if arg.endswith("point")]
    tangent_vec_args = [arg for arg in args if arg.startswith("tangent_vec")]
    for arg in point_args + tangent_vec_args:
        if arg.endswith("point"):
            code += _base_point_snippet(arg, level=level)

        # TODO: is this generic enough?
        elif arg.startswith("tangent_vec") and point_args:
            code += _tangent_point_snippet(arg, point_args[0], level=level)

    return code


def _write_generate_vec_snippet(args, level=2):
    arg_lvl = level + 1

    code = f"\n{TAB*level}vec_data = generate_vectorization_data(\n"

    kw_args = ", ".join([f"{arg}={arg}" for arg in args])
    code += f"{TAB*arg_lvl}data=[dict({kw_args}, expected=expected, atol=atol)],\n"

    vec_arg_names = ", ".join(
        [
            f'"{arg}"'
            for arg in args
            if arg.startswith("tangent_vec") or arg.endswith("point")
        ]
    )
    code += f"{TAB*arg_lvl}arg_names=[{vec_arg_names}],\n"

    code += f'{TAB*arg_lvl}expected_name="expected",\n'
    code += f"{TAB*arg_lvl}n_reps=n_reps,\n"
    code += f"{TAB*level})\n"
    code += f"{TAB*level}self._test_vectorization(vec_data)\n"

    return code


def _write_vec_test_snippet(method, level=1):
    func_name = method.short_name
    args = [arg for arg in method.args_list if arg != "self"]
    fnc_lvl = level + 1

    code = f"{TAB*level}@pytest.mark.vec\n"
    code += f"{TAB*level}def test_{func_name}_vec(self, n_reps, atol):\n"
    code += f"{TAB*fnc_lvl}{VERIFICATION_MSG}\n"

    code += _write_point_creation_snippet(args, level=fnc_lvl)

    # TODO: space or metric
    code += f"\n{TAB*fnc_lvl}expected = self.space.{func_name}({', '.join(args)})\n"

    code += _write_generate_vec_snippet(args, level=fnc_lvl)

    return code


# TODO: check (automatically) if metric or space


def write_test_method_snippets(method, has_direct_test_, has_vec_test_):
    code_snippets = {}
    if not has_direct_test_:
        code_snippets[f"test_{method.short_name}"] = _write_direct_test_snippet(method)

    if not has_vec_test_:
        code_snippets[f"test_{method.short_name}_vec"] = _write_vec_test_snippet(method)

    return code_snippets


def get_missing_imports(source_ls):
    source = "".join(source_ls)
    imports = [
        "geomstats.test.vectorization.generate_vectorization_data",
        "geomstats.test.random.get_random_tangent_vec",
    ]

    imports_ = []

    if "@pytest.mark.vec" in source:
        imports_.append("pytest")

    for import_ in imports:
        if f"{import_.split('.')[-1]}(" in source:
            imports_.append(import_)

    return imports_
