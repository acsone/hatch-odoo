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

## License

`hatch-odoo` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
