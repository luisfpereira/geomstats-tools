
# TODO: add tool to collect all the test cases from a given base
# TODO: get string to run that tests

# TODO: tool to collect all test classes (allow selection of subpackage/module)
# TODO: apply sort in the found classes

# TODO: add sanity tests


import click

_geomstats_repo_dir_option = click.option(
    '--geomstats-repo-dir', '-d', nargs=1, type=str, default=None)

_data_cls_import_option = click.option(
    '--data-cls-import', '-i', nargs=1, type=str, default=None)

_tests_loc_option = click.option('--tests-loc', '-t', nargs=1, type=str,
                                 default="tests2")


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
@click.argument('cls-import', nargs=1, type=str)
@add_options([_geomstats_repo_dir_option])
def cookiecutter_tests(cls_import, geomstats_repo_dir):
    """Creates the required objects to test a new class.
    """
    from geomstats_tools.cookiecutter_tests import create_test

    create_test(cls_import, geomstats_repo_dir=geomstats_repo_dir)


@main_cli.command()
@click.argument('cls-import', nargs=1, type=str)
@click.option('--test-cls-import', '-i', nargs=1, type=str, default=None)
@add_options([_geomstats_repo_dir_option])
def info_tests(cls_import, test_cls_import, geomstats_repo_dir):
    """Prints information about public methods and available tests.
    """
    # TODO: pass geomstats_dir to calatrava

    from geomstats_tools.info_tests import get_info_tests

    get_info_tests(cls_import, test_cls_import=test_cls_import)


@main_cli.command()
@click.argument('cls-import', nargs=1, type=str)
@add_options([
    _data_cls_import_option,
    _geomstats_repo_dir_option,
    _tests_loc_option,
])
def sort_data_methods(cls_import, data_cls_import, geomstats_repo_dir, tests_loc):
    """Sorts data methods according to test class order.

    Notes
    -----
    * Inherited methods are ignored.
    """
    from geomstats_tools.sort_data_methods import (
        sort_data_methods as sort_data_methods_,
    )
    sort_data_methods_(
        cls_import,
        data_cls_import=data_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
        tests_loc=tests_loc
    )


@main_cli.command()
@click.argument('cls-import', nargs=1, type=str)
@add_options([
    _data_cls_import_option,
    _geomstats_repo_dir_option,
    _tests_loc_option,
])
def missing_data_methods(cls_import, data_cls_import, geomstats_repo_dir, tests_loc):
    """Prints methods missing in data.

    Only considers methods for which automatic data can be generated, i.e.
    methods marker with `pytest.mark.vec` or `pytest.mark.random`.
    """
    from geomstats_tools.missing_data_methods import print_missing_data_methods

    print_missing_data_methods(
        cls_import,
        data_cls_import=data_cls_import,
        geomstats_repo_dir=geomstats_repo_dir,
        tests_loc=tests_loc
    )
