
import ast

from calatrava.parser.ast.uml import (
    PackageManager,
    Package,
)
from calatrava.parser.ast.find_imports import Module as ImportsModule

# TODO: move filters to calatrava
# TODO: need to understand how to keep it consistent


def keep_only_public_methods(methods):
    return [method for method in methods
            if method.is_public and not method.is_setter]


def remove_repeated_methods(methods):
    non_rep_methods = []
    for method in methods:
        if method.short_name not in non_rep_methods:
            non_rep_methods.append(method)

    return non_rep_methods


def keep_only_newly_defined_methods(methods, base_methods):
    base_methods_names = set([method.short_name for method in base_methods])
    return [method for method in methods if method.short_name not in base_methods_names]


def remove_properties(methods):
    return [method for method in methods if not method.is_property]


def get_classes_given_imports(imports, visitor_type="basic", packages_dir=None):
    if packages_dir is None:
        packages = [Package("geomstats", classes_visitor=visitor_type)]
    else:
        packages = [Package(package_dir, classes_visitor=visitor_type)
                    for package_dir in packages_dir]

    package_manager = PackageManager(packages)

    for cls_import in imports:
        package_manager.find(cls_import)
    package_manager.update_inheritance()

    classes = []
    for cls_import in imports:
        class_ = package_manager.get_classes()[cls_import]
        if not class_.found:
            raise Exception(f"Cannot find `{cls_import}`")

        classes.append(class_)

    return classes


def get_class_given_import(cls_import, visitor_type="basic", packages_dir=None):
    return get_classes_given_imports(
        [cls_import], visitor_type=visitor_type, packages_dir=packages_dir)[0]


class _VirtualModule(ImportsModule):
    def __init__(self, source):
        self.source = source
        super().__init__(long_name="", package=None)

    def _load_root(self):
        return ast.parse(self.source)

    @property
    def is_init(self):
        return False


def collect_imports(source):
    module = _VirtualModule(source)

    return module.get_imports()
