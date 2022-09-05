# SPDX-FileCopyrightText: 2022-present Stéphane Bidoul <stephane.bidoul@acsone.eu>
# SPDX-FileCopyrightText: 2022-present ACSONE <https://acsone.eu>
#
# SPDX-License-Identifier: MIT

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def data_path() -> Path:
    return Path(__file__).parent.joinpath("data")
