# SPDX-FileCopyrightText: 2022-present Stéphane Bidoul <stephane.bidoul@acsone.eu>
# SPDX-FileCopyrightText: 2022-present ACSONE <https://acsone.eu>
#
# SPDX-License-Identifier: MIT

from typing import Type

from hatchling.plugin import hookimpl

from .build_hook import OdooAddonsDirsBuildHook
from .metadata_hook import OdooAddonsDependenciesMetadataHook


@hookimpl
def hatch_register_build_hook() -> Type[OdooAddonsDirsBuildHook]:
    return OdooAddonsDirsBuildHook


@hookimpl
def hatch_register_metadata_hook() -> Type[OdooAddonsDependenciesMetadataHook]:
    return OdooAddonsDependenciesMetadataHook
