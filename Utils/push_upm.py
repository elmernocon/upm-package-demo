#!/usr/local/bin/python3

import re
import shutil
import subprocess
from pathlib import Path


root_path = Path(__file__).parent.parent
config_file_path = root_path / ".cz.toml"

main_branch = "main"
upm_branch = "upm"
git_path = ".git/"
package_name = "UPMPackageDemo"
package_path = f"Assets/{package_name}"


def main():
    gitignore_path = root_path / ".gitignore"
    gitignore_tmp_path = root_path / git_path / ".gitignore"

    src_path = root_path / package_path
    tmp_path = root_path / git_path / package_name
    dst_path = root_path

    version = get_version()

    if run("git", "checkout", "-f", main_branch):
        exit_with_error(f" - Failed to checkout '{main_branch}' branch.")

    print("Backing up .gitignore file and package files.")
    shutil.copy(gitignore_path, gitignore_tmp_path)
    shutil.copytree(src_path, tmp_path, dirs_exist_ok=True)
    shutil.rmtree(src_path, ignore_errors=True)

    if run("git", "checkout", "-f", upm_branch):
        exit_with_error(f" - Failed to checkout '{upm_branch}' branch.")

    if run("git", "reset", "--hard"):
        exit_with_error(f" - Failed to reset.")

    if run("git", "clean", "-d", "-f"):
        exit_with_error(" - Failed to clean.")

    if run("git", "rm", "-r", "-f", "--ignore-unmatch", "*"):
        exit_with_error(" - Failed to remove files.")

    print("Restoring .gitignore file and package files.")
    shutil.move(gitignore_tmp_path, gitignore_path)
    shutil.copytree(tmp_path, dst_path, dirs_exist_ok=True)
    shutil.rmtree(tmp_path, ignore_errors=True)

    if run("git", "add", "-A"):
        exit_with_error(" - Failed to stage files.")

    if run("git", "commit", "-m", f"UPM Release {version}"):
        exit_with_error(" - Failed to commit.")

    if run("git", "tag", f"{version}-{upm_branch}", upm_branch):
        exit_with_error(" - Failed to tag.")


def exit_with_error(error):
    print(error)
    exit(1)


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


def run(*args):
    args_list = list(args)
    print(f"Running: {' '.join(args_list)}")
    return subprocess.check_call(args_list)


if __name__ == "__main__":
    main()
