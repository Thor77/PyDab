PyDab
=====
Bundle based dotfiles manager.
Design derived from [dab](https://github.com/fd0/dab)

Installation
============
* From source
    * `git clone https://github.com/Thor77/PyDab`
    * `python setup.py install`

Usage
=====
* Initialize repository in an empty directory `dab init`
* Add bundles `dab bundle add SOURCE REFERENCE DIRECTORY`
    * Pass `--submodules` to also add submodules

Example
=======
```
$ mkdir dotfiles
$ cd dotfiles
$ dab init
$ ls
base bundles.json
```
