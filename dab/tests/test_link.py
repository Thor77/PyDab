from os import mkdir
from os.path import join as pathjoin
from os.path import exists
from shutil import rmtree

import pytest

from dab.link import link


@pytest.fixture
def target_directory(request):
    directory = 'dab/tests/target'
    mkdir(directory)

    def cleanup():
        rmtree(directory)
    request.addfinalizer(cleanup)
    return directory


def test_link(target_directory):
    link('dab/tests/__init__.py', target_directory)
    link('dab/tests/test_link.py', target_directory)
    assert exists(pathjoin(target_directory, '__init__.py'))
    assert exists(pathjoin(target_directory, 'test_link.py'))
