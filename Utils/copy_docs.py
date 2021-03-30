#!/usr/local/bin/python3

import shutil
from pathlib import Path


root_path = Path(__file__).parent.parent

target_path = "Assets/UPMPackageDemo"
doc_files = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md"
]


def main():
    print("Copying docs..")
    for doc_file in doc_files:
        src = root_path / doc_file
        dst = root_path / target_path / doc_file
        shutil.copyfile(src, dst)
        shutil.copystat(src, dst)
        print(f" - {src.relative_to(root_path)} to {dst.relative_to(root_path)}")


if __name__ == "__main__":
    main()
