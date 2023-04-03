import os

from calatrava.parser.ast.uml import (
    Package,
    PackageManager,
)

from geomstats_tools.config_utils import load_from_config
from geomstats_tools.naming_utils import (
    cls_import_to_filename,
    get_data_cls_import,
    get_test_case_cls_import,
    get_test_cls_import,
)


def from_cli_inputs_to_config(
    cls_import=None,
    test_case_cls_import=None,
    data_cls_import=None,
    test_cls_name=None,
    test_cls_import=None,
    geomstats_repo_dir=None,
    tests_loc="tests",
    classes_visitor="basic",
):

    packages_config = PackagesConfig(
        geomstats_repo_dir=geomstats_repo_dir,
        tests_loc=tests_loc,
        classes_visitor=classes_visitor,
    )

    classes_config = ClassesConfig(
        packages_config,
        cls_import=cls_import,
        test_case_cls_import=test_case_cls_import,
        data_cls_import=data_cls_import,
        test_cls_import=test_cls_import,
        test_cls_name=test_cls_name,
    )

    config = Config(classes_config)

    return config


class Config:
    def __init__(self, classes_config):
        self.classes_config = classes_config

    @property
    def packages_config(self):
        return self.classes_config.packages_config

    def get_class(self, which="main"):
        return self.classes_config.get_class(which)


class ClassesConfig:
    map_class_import = {
        "main": "cls_import",
        "test_case": "test_case_cls_import",
        "data": "data_cls_import",
        "test": "test_cls_import",
    }

    def __init__(
        self,
        packages_config,
        cls_import=None,
        test_case_cls_import=None,
        data_cls_import=None,
        test_cls_import=None,
        test_cls_name=None,
    ):

        # TODO: homogenize behavior with PackagesConfig

        self.packages_config = packages_config

        self.cls_import = cls_import
        self._test_case_cls_import = test_case_cls_import
        self._test_cls_import = test_cls_import
        self._data_cls_import = data_cls_import
        self._test_cls_import = test_cls_import

        self.test_cls_name = test_cls_name

        self._main_cls = None

    @property
    def package_manager(self):
        return self.packages_config.package_manager

    def _get_package(self, import_):
        return self.package_manager.packages[import_.split(".")[0]]

    def _get_cls_module_path(self, import_):
        package = self._get_package(import_)
        return os.path.join(package.path, cls_import_to_filename(import_))

    @property
    def test_case_cls_import(self):
        if self._test_case_cls_import is not None:
            return self._test_case_cls_import

        if self.cls_import is not None:
            self._test_case_cls_import = get_test_case_cls_import(
                self.packages_config.test_cases_loc.subpackage_import,
                self.get_class("main"),
            )
            return self._test_case_cls_import

        raise ValueError("Not enough information to get `test_case_cls_import`")

    @property
    def data_cls_import(self):
        if self._data_cls_import is not None:
            return self._data_cls_import

        # TODO: need to do some cleaning
        self._data_cls_import = get_data_cls_import(
            self.packages_config.data_loc.subpackage_import,
            self.test_case_cls_import,
        )

        return self._data_cls_import

    @property
    def test_cls_import(self):
        # TODO: can perform more complex behavior
        if self._test_cls_import is not None:
            return self._test_cls_import

        if self.cls_import is not None:
            class_ = self.get_class("main")

            self._test_cls_import = get_test_cls_import(
                self.packages_config.tests_loc.subpackage_import,
                class_,
                self.test_cls_name,
            )

            return self._test_cls_import

        raise ValueError("Not enough information to get `test_case_cls_import`")

    def get_class(self, which="main"):
        cls_import = getattr(self, self.map_class_import[which])

        class_ = self.package_manager.find(cls_import)
        self.package_manager.update_inheritance()

        return class_


class SubPackageLoc:
    def __init__(self, path_with_import, geomstats_repo_dir=None):
        if "/" not in path_with_import and geomstats_repo_dir is not None:
            path_with_import = os.path.join(geomstats_repo_dir, path_with_import)

        path_ls = path_with_import.split("/")
        import_ls = path_ls[-1].split(".")

        self.path = f"{f'{os.path.sep}'.join(path_ls[:-1])}{os.path.sep}{import_ls[0]}"
        self.package_name = import_ls[0]
        self.subpackage_import = path_ls[-1]


class PackagesConfig:
    def __init__(
        self,
        geomstats_repo_dir=None,
        tests_loc="test",
        tests_subpackage_import=None,
        test_cases_subpackage_import=None,
        data_subpackage_import=None,
        classes_visitor="basic",
    ):

        # TODO: remove tests_loc (in for backwards comp)

        if geomstats_repo_dir is None:
            geomstats_repo_dir = load_from_config("geomstats_repo_dir")

        self.geomstats_repo_dir = geomstats_repo_dir

        self.geomstats_loc = SubPackageLoc("geomstats", self.geomstats_repo_dir)

        if test_cases_subpackage_import is None:
            test_cases_subpackage_import = "geomstats.test"

        self.test_cases_loc = SubPackageLoc(
            test_cases_subpackage_import, self.geomstats_repo_dir
        )

        if tests_subpackage_import is None:
            tests_subpackage_import = f"{tests_loc}.tests_geomstats"

        self.tests_loc = SubPackageLoc(tests_subpackage_import, self.geomstats_repo_dir)

        if data_subpackage_import is None:
            data_subpackage_import = f"{self.tests_loc.package_name}.data"

        self.data_loc = SubPackageLoc(data_subpackage_import, self.geomstats_repo_dir)

        self.classes_visitor = classes_visitor

        self.package_manager = self._instantiate_package_manager()

    @property
    def packages_dir(self):
        packages_dir = []
        for loc in [
            self.geomstats_loc,
            self.test_cases_loc,
            self.tests_loc,
            self.data_loc,
        ]:
            if loc.path not in packages_dir:
                packages_dir.append(loc.path)

        return packages_dir

    def _instantiate_package_manager(self):
        packages = [
            Package(dir_, classes_visitor=self.classes_visitor)
            for dir_ in self.packages_dir
        ]

        return PackageManager(packages)
