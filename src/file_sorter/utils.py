import hashlib
import os
from pathlib import Path
from typing import Optional, Union

from loguru import logger
from rich.progress import track


def compute_hash(
    file_path: Union[str, Path], hash_algorithm: str = "sha256", buffer_size: int = 4096
) -> Optional[str]:
    """
    Compute the hash of a file.

    :param file_path: Path of the file to compute the hash.
    :param hash_algorithm: The hash algorithm type to use.
    :param buffer_size: The buffer size (in bytes) to read from the file.
    :return: The computed hash of the file or None if an error occurs.
    """
    path = Path(file_path)
    if not path.is_file():
        logger.error(f"File {file_path} does not exist or is not a valid file.")
        return None

    try:
        hash_func = hashlib.new(hash_algorithm)
    except ValueError:
        logger.error(f"The hash algorithm type {hash_algorithm} is not supported.")
        logger.debug(f"Supported hash algorithm types: {hashlib.algorithms_available}")
        return None

    try:
        with path.open("rb") as file:
            for buf in iter(lambda: file.read(buffer_size), b""):
                hash_func.update(buf)
        return hash_func.hexdigest()
    except (OSError, IOError) as e:
        logger.error(f"Error while reading file {file_path}: {e}")
        return None


def compute_hashes(
    file_paths: list[Union[str, Path]],
    hash_algorithm: str = "sha256",
    buffer_size: int = 4096,
    existing_hashes: Optional[dict[str, list[str]]] = None,
    quiet: bool = False,
) -> dict[str, list[str]]:
    """
    Compute the hashes of multiple files.

    :param file_paths: Paths of the files to compute the hashes.
    :param hash_algorithm: The hash algorithm type to use.
    :param buffer_size: The buffer size (in bytes) to read from the file.
    :param existing_hashes: A dictionary containing pre-computed hashes and their corresponding paths.
    :param quiet: If True, suppress progress display.
    :return: A dictionary containing the computed hashes and their corresponding paths.
    """
    if existing_hashes is None:
        existing_hashes = {}

    path_to_hash = {
        os.path.abspath(path): hash_value
        for hash_value, paths in existing_hashes.items()
        for path in paths
    }

    computed_hashes = {}
    iterable = (
        file_paths
        if quiet
        else track(file_paths, description="Computing hashes of files")
    )
    for file_path in iterable:
        abs_path = os.path.abspath(file_path)
        hash_value = path_to_hash.get(abs_path)
        if not hash_value:
            hash_value = compute_hash(file_path, hash_algorithm, buffer_size)
        if hash_value:
            computed_hashes.setdefault(hash_value, []).append(abs_path)

    return computed_hashes
