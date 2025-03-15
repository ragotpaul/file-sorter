import os

from file_sorter.utils import compute_hash, compute_hashes


def test_compute_hash(temp_file, compute_hash_with_cmd_func):
    # Arrange
    hash_func, hash_algorithm = compute_hash_with_cmd_func
    expected_hash = hash_func(temp_file)

    # Act
    computed_hash = compute_hash(temp_file, hash_algorithm)

    # Assert
    assert computed_hash == expected_hash


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
