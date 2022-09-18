# hatch-odoo

[![PyPI - Version](https://img.shields.io/pypi/v/hatch-odoo.svg)](https://pypi.org/project/hatch-odoo)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-odoo.svg)](https://pypi.org/project/hatch-odoo)

-----

A [hatch](https://pypi.org/project/hatch/)(ling) plugin to work with projects containing
Odoo addons. This tool will help you package a project containing Odoo addons so it can
be installed with pip:

- automatically generates dependencies based on Odoo addons manifests,
- package addons into the odoo/addons namespace independently of the source project
  layout,
- install the addons in editable mode without fiddling with `--addons-path`,

**Table of Contents**

- [hatch-odoo](#hatch-odoo)
  - [Quick start](#quick-start)
  - [Alternative project layouts](#alternative-project-layouts)
  - [License](#license)

## Quick start

Assuming you have a project containing your awesome Odoo addons at the root of your
project repository, you can set it up by creating a `pyproject.toml` file like so.

```toml
# Use the hatchling build backend, with the hatch-odoo plugin.
[build-system]
requires = ["hatchling", "hatch-odoo"]
build-backend = "hatchling.build"

[project]
name = "MyAwesomeProject"
version = "1.0"
readme = "README.md"
requires-python = ">=3.8"
# Dependencies are dynamic because they will be generated from Odoo addons manifests.
dynamic = ["dependencies"]

# Enable the hatch-odoo metadata hook to generate dependencies from addons manifests.
[tool.hatch.metadata.hooks.odoo-addons-dependencies]
# Enable the hatch-odoo build hook to package the Odoo addons into odoo/addons.
[tool.hatch.build.hooks.odoo-addons-dirs]

[tool.hatch-odoo]
# If our addons have non standard version numbers, let's help hatch-odoo discover the Odoo version.
odoo_version_override = "15.0"
# Let's add additional dependencies that are not declared in addons manifests.
dependencies = ["click-odoo-contrib"]
# Our addons are in the project root directory.
addons_dirs = ["."]
```

You can then install it in editable mode, together with its dependencies in a virtual
environment with a procedure like this:

```console
# python3 -m venv .venv
# source .venv/bin/activate
# pip install --upgrade pip setuptools wheel
# pip install -r https://raw.githubusercontent.com/odoo/odoo/15.0/requirements.txt
# pip install -e git+https://github.com/odoo/odoo@15.0
# pip install -e .
# odoo
```

All dependencies (such as OCA addons and external dependencies) declared in your project
addons manifests will be downloaded and installed from PyPI automatically.

There is no need to configure the Odoo addons path: since addons are installed in
`odoo/addons`, the regular Python import machinery works out of the box

You can then pin dependencies for reproducibility with `pip freeze` or other tools.
[pip-deepfreeze](https://pypi.org/project/pip-deepfreeze/) is known to work well with
git URLs, but other tools such as `pip-tools`, may work as well.

## Alternative project layouts

Depending on your taste and requirements, there are several alternative ways to
organize your source code. The test projects in
[tests/data](https://github.com/acsone/hatch-odoo/tree/main/tests/data) each have a
README that describe the layout and corresponding tradeoffs, with the corresponding
`pyproject.toml`.

## License

`hatch-odoo` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
