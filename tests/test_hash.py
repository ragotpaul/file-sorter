import json
import os

from click.testing import CliRunner

from file_sorter.hash import cli_hash


def test_cli_hash(temp_file, compute_hash_with_cmd_func):
    # Arrange
    hash_func, hash_algorithm = compute_hash_with_cmd_func
    expected_hash = hash_func(temp_file)

    # Act
    runner = CliRunner()
    # Act
    runner = CliRunner()
    result = runner.invoke(
        cli_hash,
        [
            temp_file,
            "--hash-algorithm",
            hash_algorithm,
        ],
    )

    # Assert
    assert result.exit_code == 0
    assert json.loads(result.output) == {expected_hash: [temp_file]}


def test_cli_hash_with_output_json(
    temp_file, compute_hash_with_cmd_func, output_json_file
):
    # Arrange
    hash_func, hash_algorithm = compute_hash_with_cmd_func
    expected_hash = hash_func(temp_file)

    # Act
    runner = CliRunner()
    result = runner.invoke(
        cli_hash,
        [
            temp_file,
            "--output-json",
            output_json_file,
            "--hash-algorithm",
            hash_algorithm,
        ],
    )

    # Assert
    assert result.exit_code == 0
    with open(output_json_file, "r") as output_file:
        hashes = json.load(output_file)
        assert len(hashes) == 1
        assert expected_hash in hashes
        assert len(hashes[expected_hash]) == 1
        assert hashes[expected_hash][0] == temp_file


def test_cli_hash_with_existing_hashes(
    temp_file, compute_hash_with_cmd_func, input_json_file
):
    # Arrange
    hash_func, hash_algorithm = compute_hash_with_cmd_func
    expected_hash = hash_func(temp_file)
    existing_hashes = {expected_hash: [temp_file]}
    with open(input_json_file, "w") as file:
        json.dump(existing_hashes, file, indent=4, sort_keys=True)

    # Act
    runner = CliRunner()
    result = runner.invoke(
        cli_hash,
        [
            temp_file,
            "--input-json",
            input_json_file,
            "--hash-algorithm",
            hash_algorithm,
        ],
    )

    # Assert
    assert result.exit_code == 0
    assert json.loads(result.output) == existing_hashes


def test_cli_hash_directory(temp_dir, compute_hash_with_cmd_func):
    # Arrange
    hash_func, hash_algorithm = compute_hash_with_cmd_func
    expected_hashes = {}
    for root, _, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            computed_hash = hash_func(file_path)
            expected_hashes.setdefault(computed_hash, []).append(file_path)

    # Act
    runner = CliRunner()
    result = runner.invoke(
        cli_hash,
        [
            temp_dir,
            "--hash-algorithm",
            hash_algorithm,
        ],
    )

    # Assert
    assert result.exit_code == 0
    assert json.loads(result.output) == expected_hashes


def test_cli_hash_directory_with_output_json(
    temp_dir, compute_hash_with_cmd_func, output_json_file
):
    # Arrange
    hash_func, hash_algorithm = compute_hash_with_cmd_func
    expected_hashes = {}
    for root, _, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            computed_hash = hash_func(file_path)
            expected_hashes.setdefault(computed_hash, []).append(file_path)

    # Act
    runner = CliRunner()
    result = runner.invoke(
        cli_hash,
        [
            temp_dir,
            "--output-json",
            output_json_file,
            "--hash-algorithm",
            hash_algorithm,
        ],
    )

    # Assert
    assert result.exit_code == 0
    with open(output_json_file, "r") as output_file:
        hashes = json.load(output_file)
        assert hashes == expected_hashes


def test_cli_hash_invalid_file(mocker, temp_file):
    # Arrange
    mocker.patch("os.path.isfile", return_value=False)

    # Act
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli_hash, [temp_file])

    # Assert
    assert result.exit_code == 1
    assert f"Error: {temp_file} is not a valid file or directory path." in result.stderr


def test_cli_hash_invalid_directory(mocker, temp_dir):
    # Arrange
    mocker.patch("os.path.isdir", return_value=False)

    # Act
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli_hash, [temp_dir])

    # Assert
    assert result.exit_code == 1
    assert f"Error: {temp_dir} is not a valid file or directory path." in result.stderr
