import os
from pathlib import Path

import pytest

from file_sorter.utils import compute_hash, compute_hashes


def test_compute_hash(temp_file, compute_hash_with_cmd_func):
    # Arrange
    hash_func, hash_algorithm = compute_hash_with_cmd_func
    expected_hash = hash_func(temp_file)

    # Act
    computed_hash = compute_hash(temp_file, hash_algorithm)

    # Assert
    assert computed_hash == expected_hash


def test_compute_hash_invalid_file():
    # Arrange
    invalid_file_path = "/invalid/path/to/file.txt"

    # Act
    result = compute_hash(invalid_file_path)

    # Assert
    assert result is None


def test_compute_hash_unsupported_algorithm(temp_file):
    # Arrange
    unsupported_algorithm = "unsupported_algo"

    # Act
    result = compute_hash(temp_file, hash_algorithm=unsupported_algorithm)

    # Assert
    assert result is None


def test_compute_hash_file_not_found(mocker, temp_file):
    # Arrange
    path = os.path.abspath(temp_file)
    mocker.patch.object(Path, "is_file", return_value=False)

    # Act
    result = compute_hash(path)

    # Assert
    assert result is None


@pytest.mark.parametrize("error", [OSError, IOError])
def test_compute_hash_file_open_error(mocker, temp_file, error):
    # Arrange
    path = os.path.abspath(temp_file)
    mocker.patch.object(Path, "open", side_effect=error)

    # Act
    result = compute_hash(path)

    # Assert
    assert result is None


def test_compute_hashes(temp_dir, compute_hash_with_cmd_func):
    # Arrange
    hash_func, hash_algorithm = compute_hash_with_cmd_func
    expected_hashes = {}
    for root, _, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            computed_hash = hash_func(file_path)
            expected_hashes.setdefault(computed_hash, []).append(file_path)

    # Act
    file_paths = []
    for root, _, files in os.walk(temp_dir):
        file_paths.extend(os.path.join(root, file) for file in files)
    computed_hashes = compute_hashes(file_paths, hash_algorithm)

    # Assert
    assert computed_hashes == expected_hashes


def test_compute_hashes_with_existing_hashes(temp_file):
    # Arrange
    existing_hashes = {"dummyhash": [str(temp_file)]}
    file_paths = [temp_file]

    # Act
    result = compute_hashes(file_paths, existing_hashes=existing_hashes)

    # Assert
    assert "dummyhash" in result
    assert len(result["dummyhash"]) == 1
    assert result["dummyhash"][0] == str(temp_file)
