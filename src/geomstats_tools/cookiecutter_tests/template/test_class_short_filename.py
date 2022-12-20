import random

import pytest

from `class_full_import` import `class_name`
from `class_test_import` import `class_name`TestCase
from geomstats.test.parametrizers import DataBasedParametrizer
from tests2.data.`class_short_filename`_data import `class_name`TestData


@pytest.fixture(
    scope="class",
    params=[
        2,
        random.randint(3, 5),
    ],
)
def spaces(request):
    request.cls.space = `class_name`(request.param)


@pytest.mark.usefixtures("spaces")
class Test`class_name`(`class_name`TestCase, metaclass=DataBasedParametrizer):
    testing_data = `class_name`TestData()
