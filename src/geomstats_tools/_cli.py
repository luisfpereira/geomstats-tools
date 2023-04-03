# TODO: add tool to collect all the test cases from a given base
# TODO: get string to run that tests

# TODO: tool to collect all test classes (allow selection of subpackage/module)
# TODO: apply sort in the found classes

# TODO: add sanity tests

# TODO: make better distinction between test and test case?

# TODO: be consistent with method names

# TODO: create better messages

# TODO: sort "_vec" methods after "normal" ones

# TODO: create given test for a given class (vec as flag)

# TODO: check if test method or data is overriden (create report?)

# TODO: bring here backends utils

# TODO: ability to create random_tests at least one after something and vice-versa?

# TODO: identify (and delete?) skips of non-existing tests

# TODO: reconstruct full class without inheritance (to consult)

# TODO: move cli tools to "script" for clear separation


import click

from geomstats_tools.calatrava_utils import forget_module
from geomstats_tools.config import from_cli_inputs_to_config

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

    # TODO: fix test name if private
    # TODO: make use of `test_cls_name`

    config = from_cli_inputs_to_config(
        cls_import=cls_import,
        test_cls_name=test_cls_name,
        test_case_cls_import=test_case_cls_import,
        data_cls_import=data_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
        tests_loc=tests_loc,
        classes_visitor="basic-methods",
    )

    out = create_test_(config)

    classe_types = ("test_case", "data", "test")

    if all(not out_ for out_ in out):
        print("Everything already exists.")
        return

    msg = "Created:"
    for class_type, out_ in zip(classe_types, out):
        if out_:
            class_ = config.get_class(class_type)
            msg += f"\n  -{class_.long_name}"

    print(msg)

    # TODO: update calatrava
    # new files may have been created
    packages_config = config.packages_config
    packages_config.package_manager = packages_config._instantiate_package_manager()

    if basic:
        return

    if out[0]:
        add_missing_test_methods(config)

    if out[1]:

        add_missing_data_methods(config)

        sort_data_methods_(config)


@main_cli.command()
@click.argument("cls-import", nargs=1, type=str)
@add_options([_test_case_cls_import_option, _geomstats_repo_dir_option])
def info_tests(cls_import, test_case_cls_import, geomstats_repo_dir):
    """Print information about public methods and available tests."""
    # TODO: check printing order
    from geomstats_tools.info_tests import print_info_tests

    config = from_cli_inputs_to_config(
        cls_import=cls_import,
        test_case_cls_import=test_case_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
        classes_visitor="basic-methods",
    )

    print_info_tests(config)


@main_cli.command()
@click.argument("test-case-cls-import", nargs=1, type=str)
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

    config = from_cli_inputs_to_config(
        test_case_cls_import=test_case_cls_import,
        data_cls_import=data_cls_import,
        tests_loc=tests_loc,
        geomstats_repo_dir=geomstats_repo_dir,
        classes_visitor="basic-methods",
    )

    data_path, data_cls_name = sort_data_methods_(config)

    print(f"Sorted `{data_cls_name}` in `{data_path}`")


@main_cli.command()
@click.argument("test-case-cls-import", nargs=1, type=str)
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

    config = from_cli_inputs_to_config(
        test_case_cls_import=test_case_cls_import,
        data_cls_import=data_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
        tests_loc=tests_loc,
        classes_visitor="basic-methods",
    )

    missing_methods_names = print_missing_data_methods(config)

    if missing_methods_names:
        indentation = " " * 2
        print("The following data methods are missing:")
        for method_name in missing_methods_names:
            print(f"{indentation}{method_name}")
    else:
        print("All data methods are defined.")


@main_cli.command()
@click.argument("test-case-cls-import", nargs=1, type=str)
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

    config = from_cli_inputs_to_config(
        test_case_cls_import=test_case_cls_import,
        data_cls_import=data_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
        tests_loc=tests_loc,
        classes_visitor="basic-methods",
    )
    data_class = config.get_class("data")

    out = add_missing_data_methods(config)

    if not out:
        print("All data methods are already defined")
        return

    msg = "Updated"
    if sort:
        sort_data_methods_(config)
        msg += " and sorted"

    msg += f" `{data_class.name}` in `{data_class.module.long_name}`"
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

    config = from_cli_inputs_to_config(
        cls_import=cls_import,
        test_case_cls_import=test_case_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
        tests_loc=tests_loc,
        classes_visitor="basic-methods",
    )

    out = add_missing_test_methods(config)

    if not out:
        print("No missing test case methods.")
        return

    test_case_class = config.get_class("test_case")

    msg = (
        f"Updated `{test_case_class.short_name}` "
        f"in `{test_case_class.module.long_name}`"
    )

    if not update_data:
        msg += "."
        print(msg)
        return

    # forget class since was updated above
    forget_module(test_case_class)

    out = add_missing_data_methods(config)
    if not out:
        msg += "."
        print(msg)
        return

    data_class = config.get_class("data")

    msg += " and corresponding data methods"
    msg += f" in `{data_class.short_name}` in `{data_class.module.long_name}`."

    if sort:
        sort_data_methods_(config)
        msg += " Data methods were also sorted."

    print(msg)
