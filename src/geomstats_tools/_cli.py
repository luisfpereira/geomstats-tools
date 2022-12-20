
import click


@click.group()
def main_cli():
    pass


@main_cli.command()
@click.argument('cls_import', nargs=1, type=str)
@click.option('--geomstats-dir', '-d', nargs=1, type=str, default=None)
def cookiecutter_tests(cls_import, geomstats_dir):
    """Creates the required objects to test a new class.
    """
    from geomstats_tools.cookiecutter_tests.script import create_test

    create_test(cls_import, geomstats_dir)
