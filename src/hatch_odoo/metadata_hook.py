# SPDX-FileCopyrightText: 2022-present Stéphane Bidoul <stephane.bidoul@acsone.eu>
# SPDX-FileCopyrightText: 2022-present ACSONE <https://acsone.eu>
#
# SPDX-License-Identifier: MIT

from typing import List

from hatchling.metadata.plugin.interface import MetadataHookInterface
from manifestoo_core.metadata import POST_VERSION_STRATEGY_NONE, metadata_from_addon_dir

from .config import iter_addon_dirs, load_hatch_odoo_config


class OdooAddonsDependenciesMetadataHook(MetadataHookInterface):
    """Hatch metadata hook to populate 'project.depencencies' from Odoo addons
    manifests."""

    PLUGIN_NAME = "odoo-addons-dependencies"

    def _get_odooo_addons_dependencies(self) -> List[str]:
        hatch_odoo_config = load_hatch_odoo_config(self.root)
        dependencies = set(hatch_odoo_config.get("dependencies", []))
        addon_dirs = list(
            iter_addon_dirs(
                self.root,
                hatch_odoo_config,
                # We don't want dependencies of addons that are not installable.
                allow_not_installable=False,
            )
        )
        depends_override = hatch_odoo_config.get("depends_override", {})
        for addon_dir in addon_dirs:
            addon_name = addon_dir.name
            # Do not add dependencies on addons that are in the project.
            depends_override[addon_name] = None
        options = dict(
            hatch_odoo_config,
            depends_override=depends_override,
            post_version_strategy_override=POST_VERSION_STRATEGY_NONE,
        )
        for addon_dir in addon_dirs:
            try:
                addon_metadata = metadata_from_addon_dir(addon_dir, options)
            except Exception as e:
                raise RuntimeError(
                    f"Error while generating metadata from {addon_dir}"
                ) from e
            addon_dependencies = addon_metadata.get_all("Requires-Dist", [])
            dependencies.update(addon_dependencies)
        return list(dependencies)

    def update(self, metadata):
        """Update the project table's metadata."""
        if "dependencies" in metadata:
            raise ValueError(
                "'dependencies' may not be listed in the 'project' table when using "
                "hatch-odoo to populate dependencies from Odoo addons manifests. "
                "If you need to add dependencies that are not in Odoo addons "
                "manifests, please use the 'tools.hatch-odoo.dependencies' key."
            )
        if "dependencies" not in metadata.get("dynamic", []):
            raise ValueError(
                "'dependencies' must be listed in 'project.dynamic' when using "
                "hatch-odoo to populate dependencies from Odoo addons manifests."
            )
        metadata["dependencies"] = self._get_odooo_addons_dependencies()
