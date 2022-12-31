"""
Install Package module.
"""
# Copyright 2019 NVIDIA CORPORATION

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import zipfile
import tempfile
import sys
import shutil
import typing

__author__ = "hfannar"
logging.basicConfig(level=logging.WARNING, format="%(message)s")
logger = logging.getLogger("install_package")


class TemporaryDirectory:
    """
    Temporary Directory.
    """

    def __init__(self) -> None:
        self.path: str = ""

    def __enter__(self) -> str:
        self.path = tempfile.mkdtemp()
        return self.path

    def __exit__(self, type_arg: typing.Any, value: typing.Any, traceback: typing.Any) -> None:
        # Remove temporary data created
        shutil.rmtree(self.path)


def install_package(package_src_path: str, package_dst_path: str) -> None:
    """
    Installs given package.

    Args:
        package_src_path (_type_): _description_
        package_dst_path (_type_): _description_
    """
    with zipfile.ZipFile(package_src_path, allowZip64=True) as zip_file, TemporaryDirectory() as temp_dir:
        zip_file.extractall(temp_dir)
        # Recursively copy (temp_dir will be automatically cleaned up on exit)
        try:
            # Recursive copy is needed because both package name and version folder could be missing in
            # target directory:
            shutil.copytree(temp_dir, package_dst_path)
        except OSError:
            logger.warning("Directory %s already present, packaged installation aborted", package_dst_path)
        else:
            logger.info("Package successfully installed to %s", package_dst_path)


install_package(sys.argv[1], sys.argv[2])
