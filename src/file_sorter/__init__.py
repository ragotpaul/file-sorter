import click

from .hash import cli_hash


@click.group()
@click.version_option()
def cli() -> None:
    pass


cli.add_command(cli_hash)
