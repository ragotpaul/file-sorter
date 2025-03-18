import json
import os

import click

from .utils import compute_hashes


@click.command(name="hash")
@click.argument(
    "paths",
    type=click.Path(exists=True),
    required=True,
    nargs=-1,
)
@click.option(
    "--input-json",
    "-i",
    "input_json_files",
    type=click.File(mode="r", encoding="utf-8"),
    multiple=True,
    help="Specify one or more JSON files containing hashes and their corresponding paths from previous runs.",
)
@click.option(
    "--output-json",
    "-o",
    "output_json_file",
    type=click.File(mode="w", encoding="utf-8"),
    help="Specify the JSON file to store the computed hashes and their corresponding paths.",
)
@click.option(
    "--hash-algorithm",
    "-t",
    type=click.Choice(["md5", "sha1", "sha256", "sha512"]),
    default="sha256",
    show_default=True,
    help="Choose the hash algorithm type to use.",
)
@click.option(
    "--buffer-size",
    "-b",
    type=click.INT,
    default=4096,
    show_default=True,
    help="Set the buffer size (in bytes) to read from the file.",
)
@click.option(
    "--progress",
    "-p",
    is_flag=True,
    help="Display progress while computing hashes.",
)
def cli_hash(
    paths, input_json_files, output_json_file, hash_algorithm, buffer_size, progress
):
    """
    Compute the hash of files.

    PATHS: Paths of files or directories containing files to compute the hash.
    """
    existing_hashes = {}
    for input_json_file in input_json_files:
        existing_hashes.update(json.load(input_json_file))

    file_paths = []
    for path in paths:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                file_paths.extend(os.path.join(root, file) for file in files)
        elif os.path.isfile(path):
            file_paths.append(path)
        else:
            raise click.ClickException(
                f"Error: {path} is not a valid file or directory path."
            )

    computed_hashes = compute_hashes(
        file_paths,
        hash_algorithm=hash_algorithm,
        buffer_size=buffer_size,
        existing_hashes=existing_hashes,
        progress=progress,
    )

    if output_json_file:
        json.dump(computed_hashes, output_json_file, indent=4, sort_keys=True)
    else:
        click.echo(json.dumps(computed_hashes, indent=4, sort_keys=True))
