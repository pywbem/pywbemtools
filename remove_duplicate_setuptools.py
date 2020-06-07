#!/usr/bin/env python
"""
This script removes duplicated dist-info directories of setuptools, which
happen to exist on the Travis CI in their Ubuntu 14.04 (trusty) distro:
  site-packages/setuptools                  <- contains 36.3.0
  site-packages/setuptools-36.0.1.dist-info <- duplicate to be removed
  site-packages/setuptools-36.3.0.dist-info
"""

import sys
import os
import re
import glob
import importlib
import shutil


def remove_duplicate_metadata_dirs(package_name):
    """Remove duplicate metadata directories of a package."""

    print("Removing duplicate metadata directories of package: %s" %
          package_name)

    module = importlib.import_module(package_name)

    py_mn = "{0}.{1}".format(sys.version_info[0], sys.version_info[1])
    print("Current Python version: {0}".format(py_mn))

    version = module.__version__
    print("Version of imported {0} package: {1}".format(package_name, version))

    site_dir = os.path.dirname(os.path.dirname(module.__file__))
    print("Site packages directory of imported package: {0}".format(site_dir))

    metadata_dirs = []
    metadata_dirs.extend(glob.glob(os.path.join(
        site_dir, '{0}-*.dist-info'.format(package_name))))
    metadata_dirs.extend(glob.glob(os.path.join(
        site_dir, '{0}-*-py{1}.egg-info'.format(package_name, py_mn))))

    for d in metadata_dirs:

        m = re.search(r'/%s-([0-9.]+)(\.di|-py)' % package_name, d)

        if not m:
            print("Warning: Could not parse metadata directory: {0}".format(d))
            continue

        d_version = m.group(1)

        if d_version == version:
            print("Found matching metadata directory: {0}".format(d))
            continue

        print("Removing duplicate metadata directory: {0}".format(d))
        shutil.rmtree(d)


if __name__ == '__main__':
    remove_duplicate_metadata_dirs('setuptools')
