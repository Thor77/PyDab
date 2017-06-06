from os import scandir
from pathlib import Path


def link(source, target_directory):
    destination = Path(target_directory, source.name)
    if not destination.exists():
        destination.symlink_to(source.path)


def link_directory(source_directory, target_directory):
    for element in scandir(source_directory):
        link(element, target_directory)
