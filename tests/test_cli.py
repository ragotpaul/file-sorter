import importlib

from click.testing import CliRunner

from file_sorter import cli


def test_cli_no_args():
    # Arrange
    runner = CliRunner()

    # Act
    result = runner.invoke(cli)

    # Assert
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_cli_help():
    # Arrange
    runner = CliRunner()

    # Act
    result = runner.invoke(cli, ["--help"])

    # Assert
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output


def test_cli_version():
    # Arrange
    runner = CliRunner()

    # Act
    result = runner.invoke(cli, ["--version"])

    # Assert
    assert result.exit_code == 0
    assert f"version {importlib.metadata.version('file_sorter')}" in result.output
