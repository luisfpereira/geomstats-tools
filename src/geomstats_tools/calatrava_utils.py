import ast
import os

from calatrava.parser.ast.find_imports import Module as ImportsModule
from calatrava.parser.ast.uml import (
    Package,
    PackageManager,
)

# TODO: move filters to calatrava
# TODO: need to understand how to keep it consistent


def keep_only_public_methods(methods):
    return [
        method
        for method in methods
        if method.is_public and not method.is_setter and "." not in method.short_name
    ]


def remove_repeated_methods(methods):
    non_rep_methods = []
    for method in methods:
        if method.short_name not in non_rep_methods:
            non_rep_methods.append(method)

    return non_rep_methods


def keep_only_newly_defined_methods(methods, base_methods):
    base_methods_names = {method.short_name for method in base_methods}
    return [method for method in methods if method.short_name not in base_methods_names]


def remove_properties(methods):
    return [method for method in methods if not method.is_property]


def class_is_defined(cls_import, package_dir):
    # TODO: needs to be different
    package = Package(package_dir, classes_visitor="basic")
    package_manager = PackageManager([package])

    package_manager.find(cls_import)
    class_ = package_manager.get_classes()[cls_import]
    return class_.found


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


def forget_module(class_):
    """Forget given module so that it can be reloaded."""
    # TODO: add this behavior to calatrava?
    class_.module.package.modules_ls.remove(class_.module)


def get_cls_module_path(class_):
    # TODO: because file does not exist; improve in calatrava
    module = class_.module
    class_import = class_.long_name
    module_import = module.long_name
    if ".".join(class_import.split(".")[:-1]) != module_import:
        return (
            os.path.join(
                module.package.path,
                f"{os.path.sep}".join(class_import.split(".")[1:-1]),
            )
            + ".py"
        )

    return module.path
