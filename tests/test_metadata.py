# SPDX-FileCopyrightText: 2022-present Stéphane Bidoul <stephane.bidoul@acsone.eu>
# SPDX-FileCopyrightText: 2022-present ACSONE <https://acsone.eu>
#
# SPDX-License-Identifier: MIT

from email import message_from_bytes
from pathlib import Path

import pytest
from build import ProjectBuilder


@pytest.mark.parametrize(
    "project_name", ["project1", "project2", "project3", "project4", "project5"]
)
def test_odoo_addons_dependencies(
    project_name: str, data_path: Path, tmp_path: Path
) -> None:
    expected_dependencies = {
        "odoo<15.1dev,>=15.0a",
        "odoo-addon-mis-builder<15.1dev,>=15.0dev",
        "wrapt",
        "click-odoo-contrib",
    }
    builder = ProjectBuilder(data_path / project_name)
    metadata_dir = builder.metadata_path(tmp_path)
    metadata_path = Path(metadata_dir) / "METADATA"
    assert metadata_path.is_file()
    metadata = message_from_bytes(metadata_path.read_bytes())
    dependencies = set(metadata.get_all("Requires-Dist"))
    assert dependencies == expected_dependencies
