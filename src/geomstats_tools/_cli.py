# TODO: add tool to collect all the test cases from a given base
# TODO: get string to run that tests

# TODO: tool to collect all test classes (allow selection of subpackage/module)
# TODO: apply sort in the found classes

# TODO: add sanity tests

# TODO: make better distinction between test and test case?

# TODO: be consistent with method names

# TODO: create better messages


import click

_geomstats_repo_dir_option = click.option(
    "--geomstats-repo-dir", "-r", nargs=1, type=str, default=None
)


_test_case_cls_import_option = click.option(
    "--test-case-cls-import", "-t", nargs=1, type=str, default=None
)

_data_cls_import_option = click.option(
    "--data-cls-import", "-d", nargs=1, type=str, default=None
)

_tests_loc_option = click.option("--tests-loc", nargs=1, type=str, default="tests2")


def add_options(options):
    # https://stackoverflow.com/a/40195800/11011913
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


@click.group()
def main_cli():
    pass


@main_cli.command()
@click.argument("cls-import", nargs=1, type=str)
@click.option("--test-cls-name", nargs=1, type=str)
@add_options(
    [
        _test_case_cls_import_option,
        _data_cls_import_option,
        _geomstats_repo_dir_option,
        _tests_loc_option,
    ]
)
@click.option("--basic", is_flag=True, default=False)
def create_test(
    cls_import,
    test_cls_name,
    test_case_cls_import,
    data_cls_import,
    geomstats_repo_dir,
    tests_loc,
    basic,
):
    """Create the required objects to test a new class."""
    from geomstats_tools.add_data_methods import add_missing_data_methods
    from geomstats_tools.add_test_methods import add_missing_test_methods
    from geomstats_tools.cookiecutter_tests import create_test as create_test_
    from geomstats_tools.sort_data_methods import (
        sort_data_methods as sort_data_methods_,
    )

    out = create_test_(
        cls_import,
        test_cls_name=test_cls_name,
        test_case_cls_import=test_case_cls_import,
        data_cls_import=data_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
        tests_loc=tests_loc,
    )

    if all(not out_[1] for out_ in out):
        print("Everything already exists.")
        return

    msg = "Created:"
    for out_ in out:
        if out_[1]:
            msg += f"\n  -{out_[0]}"
    print(msg)

    if basic:
        return

    test_case_cls_import_ = out[0][0]
    data_cls_import_ = out[1][0]

    if out[0][1]:
        add_missing_test_methods(
            cls_import,
            test_case_cls_import=test_case_cls_import_,
            geomstats_repo_dir=geomstats_repo_dir,
        )

    if out[1][1]:

        add_missing_data_methods(
            test_case_cls_import_,
            data_cls_import=data_cls_import_,
            geomstats_repo_dir=geomstats_repo_dir,
            tests_loc=tests_loc,
        )

        sort_data_methods_(
            test_case_cls_import_,
            data_cls_import=data_cls_import_,
            geomstats_repo_dir=geomstats_repo_dir,
            tests_loc=tests_loc,
        )


@main_cli.command()
@click.argument("cls-import", nargs=1, type=str)
@add_options([_test_case_cls_import_option, _geomstats_repo_dir_option])
def info_tests(cls_import, test_case_cls_import, geomstats_repo_dir):
    """Print information about public methods and available tests."""
    from geomstats_tools.info_tests import print_info_tests

    print_info_tests(
        cls_import,
        test_case_cls_import=test_case_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
    )


@main_cli.command()
@click.argument("test-cls-import", nargs=1, type=str)
@add_options(
    [
        _data_cls_import_option,
        _geomstats_repo_dir_option,
        _tests_loc_option,
    ]
)
def sort_data_methods(
    test_case_cls_import, data_cls_import, geomstats_repo_dir, tests_loc
):
    """Sort data methods according to test class order.

    Notes
    -----
    * Inherited methods are ignored.
    """
    from geomstats_tools.sort_data_methods import (
        sort_data_methods as sort_data_methods_,
    )

    data_path, data_cls_name = sort_data_methods_(
        test_case_cls_import,
        data_cls_import=data_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
        tests_loc=tests_loc,
    )

    print(f"Sorted `{data_cls_name}` in `{data_path}`")


@main_cli.command()
@click.argument("test-cls-import", nargs=1, type=str)
@add_options(
    [
        _data_cls_import_option,
        _geomstats_repo_dir_option,
        _tests_loc_option,
    ]
)
def missing_data_methods(
    test_case_cls_import, data_cls_import, geomstats_repo_dir, tests_loc
):
    """Print methods missing in data.

    Only considers methods for which automatic data can be generated, i.e.
    methods marker with `pytest.mark.vec` or `pytest.mark.random`.
    """
    from geomstats_tools.missing_data_methods import print_missing_data_methods

    missing_methods_names = print_missing_data_methods(
        test_case_cls_import,
        data_cls_import=data_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
        tests_loc=tests_loc,
    )

    if missing_methods_names:
        indentation = " " * 2
        print("The following data methods are missing:")
        for method_name in missing_methods_names:
            print(f"{indentation}{method_name}")
    else:
        print("All data methods are defined.")


@main_cli.command()
@click.argument("test-cls-import", nargs=1, type=str)
@add_options(
    [
        _data_cls_import_option,
        _geomstats_repo_dir_option,
        _tests_loc_option,
    ]
)
@click.option("--sort", "-s", is_flag=True, default=False)
def add_data_methods(
    test_case_cls_import, data_cls_import, geomstats_repo_dir, tests_loc, sort
):
    """Add missing data methods for `vec` and `random`."""
    from geomstats_tools.add_data_methods import add_missing_data_methods
    from geomstats_tools.sort_data_methods import (
        sort_data_methods as sort_data_methods_,
    )

    out = add_missing_data_methods(
        test_case_cls_import,
        data_cls_import=data_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
        tests_loc=tests_loc,
    )
    if out is None:
        print("All data methods are already defined")
        return

    data_path, data_cls_name = out

    msg = "Updated"
    if sort:
        sort_data_methods_(
            test_case_cls_import,
            data_cls_import=data_cls_import,
            geomstats_repo_dir=geomstats_repo_dir,
            tests_loc=tests_loc,
        )
        msg += " and sorted"

    msg += f" `{data_cls_name}` in `{data_path}`"
    print(msg)


@main_cli.command()
@click.argument("cls-import", nargs=1, type=str)
@add_options(
    [
        _test_case_cls_import_option,
        _data_cls_import_option,
        _geomstats_repo_dir_option,
        _tests_loc_option,
    ]
)
@click.option("--update-data", "-u", is_flag=True, default=False)
@click.option("--sort", "-s", is_flag=True, default=False)
def add_test_methods(
    cls_import,
    test_case_cls_import,
    data_cls_import,
    geomstats_repo_dir,
    tests_loc,
    update_data,
    sort,
):
    """Add missing test methods.

    Notes
    -----
    * "Normal" and `vec` tests are added.
    * data can be updated if requested.
    * sorting can be done if requested.
    """
    from geomstats_tools.add_data_methods import add_missing_data_methods
    from geomstats_tools.add_test_methods import add_missing_test_methods
    from geomstats_tools.sort_data_methods import (
        sort_data_methods as sort_data_methods_,
    )

    out = add_missing_test_methods(
        cls_import,
        test_case_cls_import=test_case_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
    )

    if out is None:
        print("No missing test case methods.")
        return

    test_path, test_case_cls_import, test_cls_name = out
    msg = f"Updated `{test_cls_name}` in `{test_path}`"

    if not update_data:
        msg += "."
        print(msg)
        return

    out = add_missing_data_methods(
        test_case_cls_import,
        data_cls_import=data_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
        tests_loc=tests_loc,
    )
    if out is None:
        msg += "."
        print(msg)
        return
    data_path, data_cls_name = out

    msg += " and corresponding data methods"
    msg += f" in `{data_cls_name}` in `{data_path}`."

    if sort:
        sort_data_methods_(
            test_case_cls_import,
            data_cls_import=data_cls_import,
            geomstats_repo_dir=geomstats_repo_dir,
            tests_loc=tests_loc,
        )
        msg += " Data methods were also sorted."

    print(msg)
