# SPDX-FileCopyrightText: 2022-present Stéphane Bidoul <stephane.bidoul@acsone.eu>
# SPDX-FileCopyrightText: 2022-present ACSONE <https://acsone.eu>
# SPDX-FileCopyrightText: 2025-present XCG SAS <https://orbeet.io>
#
# SPDX-License-Identifier: MIT

import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Tuple

import pytest


@pytest.mark.parametrize(
    "project, addons_only, addon_names",
    [
        ("project1", False, ("addona", "addonb", "addon_uninstallable")),
        ("project2", False, ("addona", "addonb", "addon_uninstallable")),
        ("project3", False, ("addona", "addonb", "addon_uninstallable")),
        ("project4", False, ("addona", "addonb", "addon_uninstallable")),
        ("project5", False, ("addona", "addonb", "addon_uninstallable")),
        ("project6", True, ("addona", "addonb", "addon_uninstallable")),
        ("project7", True, ("project7",)),
    ],
)
@pytest.mark.parametrize("build_via_sdist", [True, False])
def test_build(
    project: str,
    addons_only: bool,
    addon_names: Tuple[str],
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
        for addon_name in addon_names:
            assert f"odoo/addons/{addon_name}/__init__.py" in files
            assert f"odoo/addons/{addon_name}/__manifest__.py" in files
        assert addons_only or f"{project}/__init__.py" in files
