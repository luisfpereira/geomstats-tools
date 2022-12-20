from geomstats_tools.config_utils import load_from_config

from .utils import (
    get_base_class_names,
    get_placeholders,
    get_updated_codes,
    get_class_given_import,
    output_to_files,
)


def create_test(cls_import, geomstats_repo_dir=None):
    # TODO: better placeholds may be required

    if geomstats_repo_dir is None:
        geomstats_repo_dir = load_from_config("geomstats_repo_dir")

    class_ = get_class_given_import(cls_import)
    base_names = get_base_class_names(class_)
    placeholders = get_placeholders(cls_import, base_names)

    filenames = [
        "test_class_short_filename.py",
        "class_short_filename.py",
        "class_short_filename_data.py"
    ]

    codes = get_updated_codes(placeholders, filenames)

    output_to_files(codes, geomstats_repo_dir, cls_import)
