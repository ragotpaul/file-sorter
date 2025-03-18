import os
import subprocess
import tempfile

import pytest


@pytest.fixture(params=[1, 64, 1024, 4096, 8192])
def temp_file(request):
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(os.urandom(request.param))
        yield temp_file.name


@pytest.fixture(
    params=[
        {
            "": [("file1.txt", 1024)],
            "subdir1": [("file2.txt", 4096)],
            os.path.join("subdir1", "subdir2"): [("file3.txt", 8192)],
        },
        {
            "": [("file1.txt", 64), ("file2.txt", 1024)],
            "subdir1": [("file3.txt", 4096), ("file4.txt", 8192)],
        },
        {"": [("file1.txt", 1024), ("file2.txt", 4096), ("file3.txt", 8192)]},
    ]
)
def temp_dir(request):
    with tempfile.TemporaryDirectory() as temp_dir:
        structure = request.param
        for path, files in structure.items():
            dir_path = os.path.join(temp_dir, path)
            os.makedirs(dir_path, exist_ok=True)
            for file_name, file_size in files:
                file_path = os.path.join(dir_path, file_name)
                with open(file_path, "wb") as f:
                    f.write(os.urandom(file_size))
        yield temp_dir
        for root, _, files in os.walk(temp_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            os.rmdir(root)


@pytest.fixture(
    params=[
        "md5",
        "sha1",
        "sha256",
        "sha512",
    ]
)
def compute_hash_with_cmd_func(request):
    def compute_hash_with_cmd_(file_path: str) -> str:
        cmd = f"{request.param}sum {file_path}"
        result = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.stdout.decode().split()[0]

    return compute_hash_with_cmd_, request.param


@pytest.fixture
def json_file():
    with tempfile.NamedTemporaryFile(suffix=".json") as temp_file:
        yield temp_file.name


@pytest.fixture
def output_json_file(json_file):
    return json_file


@pytest.fixture
def input_json_file(json_file):
    return json_file
