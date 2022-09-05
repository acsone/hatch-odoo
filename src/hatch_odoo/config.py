# SPDX-FileCopyrightText: 2022-present Stéphane Bidoul <stephane.bidoul@acsone.eu>
#
# SPDX-License-Identifier: MIT

import sys
from pathlib import Path
from typing import Iterator

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib

from manifestoo_core.addon import is_addon_dir


def get_project_name(root: str) -> str:
    pyproject_toml = Path(root) / "pyproject.toml"
    pyproject = tomllib.loads(pyproject_toml.read_text(encoding="utf-8"))
    return pyproject["project"]["name"]


def load_hatch_odoo_config(root: str) -> dict:
    pyproject_toml = Path(root) / "pyproject.toml"
    pyproject = tomllib.loads(pyproject_toml.read_text(encoding="utf-8"))
    return pyproject.get("tool", {}).get("hatch-odoo", {})


def iter_addons_dirs(root: str, config: dict) -> Iterator[Path]:
    addons_dirs = config.get("addons_dirs")
    if not addons_dirs:
        raise RuntimeError("missing tools.hatch-odoo.addons_dir in pyproject.toml")
    for addons_dir in [Path(root) / d for d in addons_dirs]:
        if not addons_dir.is_dir():
            continue
        yield addons_dir


def iter_addon_dirs(
    root: str,
    config: dict,
    allow_not_installable: bool,
) -> Iterator[Path]:
    for addons_dir in iter_addons_dirs(root, config):
        for addon_dir in addons_dir.iterdir():
            if is_addon_dir(addon_dir, allow_not_installable=allow_not_installable):
                yield addon_dir
