
import click


@click.group()
def main_cli():
    pass


@main_cli.command()
@click.argument('cls-import', nargs=1, type=str)
@click.option('--geomstats-dir', '-d', nargs=1, type=str, default=None)
def cookiecutter_tests(cls_import, geomstats_dir):
    """Creates the required objects to test a new class.
    """
    from geomstats_tools.cookiecutter_tests.script import create_test

    create_test(cls_import, geomstats_dir)


@main_cli.command()
@click.argument('cls-import', nargs=1, type=str)
@click.option('--test-cls-import', '-t', nargs=1, type=str, default=None)
@click.option('--geomstats-dir', '-d', nargs=1, type=str, default=None)
def info_tests(cls_import, test_cls_import, geomstats_dir):
    """Prints information relative to public methods and available tests.
    """
    # TODO: pass geomstats_dir to calatrava

    from geomstats_tools.info_tests.script import get_info_tests

    get_info_tests(cls_import, test_cls_import)
