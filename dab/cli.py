from os import environ

import click

from dab.bundles import Bundles


@click.group()
@click.option('--dry-run', help='Only print actions', type=bool, default=False)
@click.pass_context
def cli(ctx, dry_run):
    ctx.obj = {}
    ctx.obj['dry_run'] = dry_run
    ctx.obj['bundles'] = Bundles.load()


@cli.command()
@click.pass_context
def init(ctx):
    '''
    Initialize dab repository
    '''
    ctx.obj['bundles'].init()


@cli.command()
@click.argument('bundles', nargs=-1)
@click.option(
    '--target', help='Target directory', type=click.Path(exists=True)
)
@click.pass_context
def install(ctx, bundles, target):
    '''
    Install one or multiple bundles
    '''
    if not bundles:
        click.echo('No bundles selected')
        return
    if not target:
        target = environ['HOME']
    for bundle in bundles:
        click.echo('Installing {} to {}'.format(bundle, target))
        ctx.obj['bundles'].install(bundle, target)


@cli.group()
@click.pass_context
def bundle(ctx):
    '''
    Manage bundles.json
    '''
    pass


@bundle.command()
@click.argument('source')
@click.argument('reference')
@click.argument('directory')
@click.option('--submodules', help='Add submodules', is_flag=True)
@click.pass_context
def add(ctx, source, reference, directory, submodules):
    '''
    Add a bundle
    '''
    ctx.obj['bundles'].add(source, reference, directory)
    if submodules:
        ctx.obj['bundles'].add_submodules(directory)


@bundle.command()
@click.pass_context
def update(ctx):
    '''
    Update bundles
    '''
    ctx.obj['bundles'].update()
