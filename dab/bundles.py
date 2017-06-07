import json
from collections import namedtuple
from os import makedirs
from os.path import join as pathjoin
from os.path import abspath, basename, exists, relpath
from subprocess import run

from dab.link import link_directory

Bundle = namedtuple('Bundle', ['source', 'ref', 'dir'])


def bundle_hook(obj):
    if type(obj) == dict:
        keys = [key.lower() for key in obj.keys()]
        for field in Bundle._fields:
            if field not in keys:
                return obj
        else:
            return Bundle(*obj.values())


class Bundles(object):
    def __init__(self, bundles=[], basedir='.'):
        self.bundles = bundles
        self.basedir = abspath(basedir)

    @classmethod
    def load(cls, basedir='.'):
        '''
        Load Bundles from config at basedir/bundles.json

        :param basedir: base directory
        :type basedir: str

        :return: Bundles loaded from config
        :rtype dab.bundles.Bundles
        '''
        path = pathjoin(basedir, 'bundles.json')
        if not exists(path):
            return cls(basedir=basedir)
        obj = {}
        with open(path, 'r') as f:
            obj = json.load(f, object_hook=bundle_hook)
        return cls(obj.get('bundles', obj.get('Bundles', [])), basedir)

    def _save(self, path=None, compat=True):
        '''
        Save Bundles to path

        :param path: path to target file
        :param compat: Write in compatability mode (for use with go-impl)

        :type path: str
        :type compat: bool
        '''
        if not path:
            path = pathjoin(self.basedir, 'bundles.json')
        bundles = map(
            lambda b: b._asdict(),
            self.bundles
        )
        if compat:
            bundles = map(
                lambda b: {k.capitalize(): v for k, v in b.items()},
                bundles
            )
        obj = {'Bundles' if compat else 'bundles': list(bundles)}
        with open(path, 'w') as f:
            json.dump(obj, f)

    def init(self):
        '''
        Initialize repo for version control and create base package
        '''
        # create contents
        makedirs(pathjoin(self.basedir, 'base'), exist_ok=True)
        self._save()

        # version control
        run(['git', 'init', '-q'])
        run(['git', 'add', 'bundles.json', 'base/'])
        run(['git', 'commit', '--message', 'Initial commit'])

    def add(self, source, reference, directory):
        '''
        Add a Bundle to this collection

        :param source: source url or path
        :param reference: reference of the source
        :param directory: target directory

        :type source: str
        :type reference: str
        :type directory: str
        '''
        directory = relpath(pathjoin(self.basedir, directory))
        self.bundles.append(Bundle(source, reference, directory))

        # fetch contents
        run([
            'git', '-c', 'fetch.fsckObjects=false', 'subtree', 'add',
            '--squash', '--prefix', directory, source, reference
        ])

        # version control changes to bundles.json
        self._save()
        run(['git', 'add', pathjoin(self.basedir, 'bundles.json')])
        message = 'Add bundle as {}\n\nSourced from {} ({})\n'.format(
            directory, source, reference
        )
        run(['git', 'commit', '--message', message, 'bundles.json'])

    def update(self):
        '''
        Update all bundles
        '''
        for bundle in self.bundles:
            run([
                'git', '-c', 'fetch.fsckObjects=false', 'subtree', 'pull',
                '-q', '--squash', '--prefix',
                bundle.dir, bundle.source, bundle.ref
            ])

    def install(self, bundle, target):
        '''
        Install `bundle` to `target`

        :param bundle: bundle to install
        :param target: target directory for installation

        :type bundle: str
        :type target: str
        '''
        bundle_directory = pathjoin(self.basedir, bundle)
        if not exists(bundle_directory):
            raise Exception('Bundle {} does not exist'.format(bundle))
        # link all files in bundle_directory to target
        link_directory(bundle_directory, target)
