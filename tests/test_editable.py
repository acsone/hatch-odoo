# SPDX-FileCopyrightText: 2022-present Stéphane Bidoul <stephane.bidoul@acsone.eu>
# SPDX-FileCopyrightText: 2022-present ACSONE <https://acsone.eu>
#
# SPDX-License-Identifier: MIT

import subprocess
import sys
from pathlib import Path
from typing import List

import pytest


@pytest.mark.parametrize(
    "project_name,expected_editable_pth_lines",
    [
        ("project1", ["src"]),
        ("project2", ["src", "build/__editable_odoo_addons__"]),
        ("project3", [""]),
        ("project4", ["", "addons_group1", "addons_group2"]),
        ("project5", ["", "build/__editable_odoo_addons__"]),
    ],
)
def test_odoo_addons_dependencies(
    project_name: str,
    expected_editable_pth_lines: List[str],
    data_path: Path,
    tmp_path: Path,
) -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-e",
            str(data_path / project_name),  # str for compat with Python 3.7 on Windows
            "--no-deps",
            "--no-build-isolation",
            "--target",
            str(tmp_path),  # str for compat with Python 3.7 on Windows
        ],
        check=True,
    )
    # Check we have the .pth lines we expect.
    pth_lines = set()
    for pth_file in tmp_path.glob("*.pth"):
        pth_lines.update((tmp_path / pth_file).read_text().splitlines())
    assert pth_lines == {
        str(data_path / project_name / line) for line in expected_editable_pth_lines
    }
    # Check all addons are in the editable paths.
    expected_editable_addon_names = ["addona", "addonb"]
    editable_addon_names = []
    for pth_line in pth_lines:
        addons_dir = Path(pth_line) / "odoo" / "addons"
        for addon_name in expected_editable_addon_names:
            if (addons_dir / addon_name).is_dir():
                editable_addon_names.append(addon_name)
    assert sorted(editable_addon_names) == expected_editable_addon_names
