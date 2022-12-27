from geomstats_tools.args_manip import update_geomstats_repo_dir

from geomstats_tools.calatrava_utils import get_class_given_import
from .utils import (
    get_base_class_names,
    get_placeholders,
    get_updated_codes,
    output_to_files,
)


@update_geomstats_repo_dir
def create_test(cls_import, *, geomstats_repo_dir=None):
    # TODO: better placeholds may be required

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
