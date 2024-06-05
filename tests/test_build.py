# SPDX-FileCopyrightText: 2022-present Stéphane Bidoul <stephane.bidoul@acsone.eu>
# SPDX-FileCopyrightText: 2022-present ACSONE <https://acsone.eu>
#
# SPDX-License-Identifier: MIT

import subprocess
import sys
import zipfile
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "project, addons_only",
    [
        ("project1", False),
        ("project2", False),
        ("project3", False),
        ("project4", False),
        ("project5", False),
        ("project6", True),
    ],
)
@pytest.mark.parametrize("build_via_sdist", [True, False])
def test_build(
    project: str,
    addons_only: bool,
    build_via_sdist: bool,
    data_path: Path,
    tmp_path: Path,
) -> None:
    build_cmd = [
        sys.executable,
        "-m",
        "build",
        "-n",
        "-o",
        str(tmp_path),  # str for compat with Python 3.7 on Windows
    ]
    if not build_via_sdist:
        build_cmd.append("-w")
    subprocess.run(
        build_cmd,
        check=True,
        cwd=data_path / project,
    )
    wheel_file = next(tmp_path.glob(f"{project}-*.whl"))
    with zipfile.ZipFile(wheel_file) as zip_file:
        files = set(zip_file.namelist())
        for addon_name in ("addona", "addonb", "addon_uninstallable"):
            assert f"odoo/addons/{addon_name}/__init__.py" in files
            assert f"odoo/addons/{addon_name}/__manifest__.py" in files
        assert addons_only or f"{project}/__init__.py" in files
