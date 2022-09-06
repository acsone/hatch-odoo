# project5

A project with Odoo addons grouped in several directories, with additional packages at
the project root.

This layout is for large projects where there are to many addons to comfortably handle
in one directory. Editable installs use symbolic links since addons are not in
`odoo/addons` directories. If you dislike these symlinks, please look at `project4` for
a layout that installs more naturally in editable mode.
