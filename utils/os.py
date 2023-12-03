import os
import importlib


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def write_file(file_path, data):
    with open(file_path, "wb" if isinstance(data, bytes) else "w") as file:
        file.write(data)


def make_dir(dir_path):
    os.makedirs(dir_path, exist_ok=True)


def import_module_from_file(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
