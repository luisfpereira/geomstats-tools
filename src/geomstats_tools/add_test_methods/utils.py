from geomstats_tools.naming_utils import (
    has_direct_test,
    has_vec_test,
)

# TODO: better strategy than replace? lazy evaluation

TAB = " " * 4


def collect_methods_info(cls_methods, tested_methods_names):
    tested_methods_names = set(tested_methods_names)

    methods_info = {}
    for method in cls_methods:
        has_direct_test_ = has_direct_test(method.short_name, tested_methods_names)
        has_vec_test_ = has_vec_test(method.short_name, tested_methods_names)

        if not (has_direct_test_ and has_vec_test_):
            methods_info[method.short_name] = {
                "method": method,
                "has_direct_test": has_direct_test_,
                "has_vec_test": has_vec_test_,
            }

    return methods_info


VERIFICATION_MSG = "# TODO: generated automatically. check if correct"

DIRECT_TEST_CODE_SNIPPET = f"""    def test_`func_name`(self, `args_list`, expected, atol):
        {VERIFICATION_MSG}
        res = self.space.`func_name`(`args_list`)
        self.assertAllClose(res, expected, atol=atol)
"""


def _write_direct_test_snippet(method):
    args = [arg for arg in method.args_list if arg != "self"]
    code = (DIRECT_TEST_CODE_SNIPPET
            .replace("`func_name`", method.short_name)
            .replace("`args_list`", ", ".join(args))
            )

    return code


def _base_point_snippet(arg_name, left_space=TAB * 2):
    return f"{left_space}{arg_name} = self.space.random_point()\n"


def _tangent_point_snippet(arg_name, base_point="base_point", left_space=TAB * 2):
    return f"{left_space}{arg_name} = get_random_tangent_vec(self.space, {base_point})\n"


def _write_vec_test_snippet(method):
    # TODO: add indentation later?
    # TODO: split in shorter functions

    func_name = method.short_name
    args = [arg for arg in method.args_list if arg != "self"]

    code = f"{TAB}@pytest.mark.vec\n"
    code += f"{TAB}def test_{func_name}_vec(self, n_reps, atol):\n"
    code += f"{2*TAB}{VERIFICATION_MSG}\n"

    point_args = [arg for arg in args if arg.endswith("point")]
    tangent_vec_args = [arg for arg in args if arg.startswith("tangent_vec")]
    for arg in point_args + tangent_vec_args:
        if arg.endswith("point"):
            code += _base_point_snippet(arg)

        # TODO: is this generic enough?
        elif arg.startswith("tangent_vec"):
            code += _tangent_point_snippet(arg, point_args[0])

    # TODO: space or metric
    code += f"\n{TAB*2}expected = self.space.{func_name}({', '.join(args)})\n"

    code += f"\n{TAB*2}vec_data = generate_vectorization_data(\n"

    kw_args = ', '.join([f"{arg}={arg}" for arg in args])
    code += f"{TAB*3}data = dict({kw_args}, expected=expect, atol=atol),\n"

    vec_arg_names = ", ".join([f'"{arg}"' for arg in args
                               if arg.startswith("tangent_vec") or arg.endswith("point")])
    code += f"{TAB*3}arg_names=[{vec_arg_names}],\n"

    code += f'{TAB*3}expected_name="expected",\n'
    code += f"{TAB*3}n_reps=n_reps,\n"
    code += f"{TAB*2})\n"
    code += f"{TAB*2}self._test_vectorization(vec_data)\n"

    return code


# TODO: check (automatically) if metric or space
# TODO: need to consider imports for vectorized (pytest and generate_vectorized_data)


def write_test_method_snippets(method, has_direct_test_, has_vec_test_):
    code_snippets = {}
    if not has_direct_test_:
        code_snippets[f"test_{method.short_name}"] = _write_direct_test_snippet(method)

    if not has_vec_test_:
        code_snippets[f"test_{method.short_name}_vec"] = _write_vec_test_snippet(method)

    return code_snippets
