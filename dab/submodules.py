from collections import namedtuple
from configparser import ConfigParser
from os.path import join as pathjoin
from os.path import exists
from pathlib import Path

Submodule = namedtuple('Submodule', ['url', 'path'])


def find(path):
    submodules_location = pathjoin(path, '.gitmodules')
    if not exists(submodules_location):
        return []
    config = ConfigParser()
    config.read(submodules_location)
    submodules = []
    for section in config.sections():
        if not section.startswith('submodule'):
            continue
        submodule_url = config.get(section, 'url')
        submodule_path = config.get(section, 'path')
        if not submodule_url or not submodule_path:
            continue
        submodules.append(Submodule(submodule_url, submodule_path))
    return submodules
