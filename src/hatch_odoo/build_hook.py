# SPDX-FileCopyrightText: 2022-present Stéphane Bidoul <stephane.bidoul@acsone.eu>
# SPDX-FileCopyrightText: 2022-present ACSONE <https://acsone.eu>
#
# SPDX-License-Identifier: MIT

import atexit
import shutil
import tempfile
from pathlib import Path
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

from .config import get_project_name, iter_addon_dirs, load_hatch_odoo_config


class OdooAddonsDirsBuildHook(BuildHookInterface):
    """Hatch build hook to add Odoo addons directories to the wheel, and available as
    symlinks in sys.path in editable mode."""

    PLUGIN_NAME = "odoo-addons-dirs"

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        if self.target_name != "wheel":
            return
        hatch_odoo_config = load_hatch_odoo_config(self.root)
        if version == "standard":
            force_include = build_data["force_include"]
            for addon_dir in iter_addon_dirs(
                self.root,
                hatch_odoo_config,
                # We force-include addons that are installable False to avoid that the
                # default hatch behaviour adds them at the wrong place in the wheel.
                allow_not_installable=True,
            ):
                addon_name = addon_dir.name
                force_include[addon_dir] = f"odoo/addons/{addon_name}"
        elif version == "editable" and self.config.get("editable_symlinks", True):
            editable_path = Path(self.root) / "build" / "__editable_odoo_addons__"
            if editable_path.is_dir():
                shutil.rmtree(editable_path)
            editable_odoo_addons_path = editable_path / "odoo" / "addons"
            has_editable_symlinks = False
            for addon_dir in iter_addon_dirs(
                self.root,
                hatch_odoo_config,
                allow_not_installable=False,
            ):
                # Symlink the addon in the editable path.
                if not has_editable_symlinks:
                    editable_odoo_addons_path.mkdir(parents=True)
                    has_editable_symlinks = True
                addon_name = addon_dir.name
                editable_addon_path = editable_odoo_addons_path / addon_name
                editable_addon_path.symlink_to(addon_dir)
            # Add .pth to build/__editable_odoo_addons__ in wheel.
            if has_editable_symlinks:
                with tempfile.NamedTemporaryFile(
                    mode="w", encoding="utf-8", delete=False
                ) as pth_file:
                    atexit.register(Path(pth_file.name).unlink)
                    pth_file.write(str(editable_path) + "\n")
                project_name = get_project_name(self.root)
                force_include_editable = build_data["force_include_editable"]
                force_include_editable[pth_file.name] = (
                    f"{project_name}_editable_odoo_addons.pth"
                )
