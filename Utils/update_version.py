#!/usr/local/bin/python3

import fileinput
import json
import re
import shutil
import subprocess
from pathlib import Path

root_path = Path(__file__).parent.parent
config_file_path = root_path / ".cz.toml"


package_name = "UPMPackageDemo"
package_path = f"Assets/{package_name}"
package_json_path = root_path / package_path / "package.json"
project_settings_path = root_path / "ProjectSettings" / "ProjectSettings.asset"


def main():
    version = get_version()
    set_version_package_json(version)
    set_version_project_settings(version)


def get_version():
    def ask_version():
        return input("Input version: ")
    if not config_file_path.exists():
        return ask_version()
    config_text = config_file_path.read_text()
    match = re.search(r"version\s*=\s*\"(.*)\"", config_text)
    if not match:
        return ask_version()
    return match.group(1)


def set_version_package_json(version):
    if not package_json_path.exists():
        return
    package_json_text = package_json_path.read_text()
    package_json = json.loads(package_json_text)
    package_json["version"] = version
    package_json_text = json.dumps(package_json, indent=2)
    package_json_path.write_text(package_json_text)
    print(f"Updated package.json")


def set_version_project_settings(version):
    if not project_settings_path.exists():
        return
    pattern = "  bundleVersion: "
    with fileinput.FileInput(str(project_settings_path.resolve()), inplace=True) as file_input:
        for line in file_input:
            if line.startswith(pattern):
                line = f"{pattern}{version}\n"
            print(line, end="")
    print(f"Updated ProjectSettings.asset")


if __name__ == "__main__":
    main()
