
from calatrava.parser.ast.uml import (
    PackageManager,
    Package,
)


def get_classes_given_imports(imports, visitor_type="basic"):
    package = Package("geomstats", classes_visitor=visitor_type)
    package_manager = PackageManager([package])

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


def get_class_given_import(cls_import, visitor_type="basic"):
    return get_classes_given_imports(
        [cls_import], visitor_type=visitor_type)[0]
