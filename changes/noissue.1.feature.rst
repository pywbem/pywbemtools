Development: Migrated from setup.py to pyproject.toml since that is the
recommended direction for Python packages. The make targets have not changed.
The content of the wheel and source distribution archives has not changed.

Some files have been renamed:
- minimum-constraints.txt to minimum-constraints-develop.txt
- .safety-policy-all.yml to .safety-policy-develop.yml

Removed pywbem/_version_scm.py from git tracking, because it is now
dynamically created when building the distribution.
