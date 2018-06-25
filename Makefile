# ------------------------------------------------------------------------------
# Makefile for pybemtools repository of pywbem project
#
# Supported OS platforms for this makefile:
#     Linux (any distro)
#     OS-X
#     Windows with UNIX-like env such as CygWin (with Python in UNIX-like env)
#     native Windows (with Python in Windows)
#
# Prerequisites for running this makefile:
#   These commands are used on all supported OS platforms:
#     make (GNU make)
#     bash
#     echo, rm, mv, find, xargs, tee, touch, chmod, wget
#     python (This Makefile uses the active Python environment, virtual Python
#        environments are supported)
#     pip (in the active Python environment)
#     twine (in the active Python environment)
#   These additional commands are used on Linux, OS-X and Windows with UNIX env:
#     uname
#   These additional commands are used on native Windows:
#     cmd
# ------------------------------------------------------------------------------

# Python / Pip commands
ifndef PYTHON_CMD
  PYTHON_CMD := python
endif
ifndef PIP_CMD
  PIP_CMD := pip
endif

# Package level
ifndef PACKAGE_LEVEL
  PACKAGE_LEVEL := latest
endif
ifeq ($(PACKAGE_LEVEL),minimum)
  pip_level_opts := -c minimum-constraints.txt
else
  ifeq ($(PACKAGE_LEVEL),latest)
    pip_level_opts := --upgrade
  else
    $(error Error: Invalid value for PACKAGE_LEVEL variable: $(PACKAGE_LEVEL))
  endif
endif

# Determine OS platform make runs on
ifeq ($(OS),Windows_NT)
  PLATFORM := Windows
else
  # Values: Linux, Darwin
  PLATFORM := $(shell uname -s)
endif

# Determine if coverage details report generated
# The variable can be passed in as either an environment variable or
# command line variable. When set, generates a set of reports of the
# pywbem/*.py files showing line by line coverage.
ifdef COVERAGE_REPORT
  coverage_report := --cov-report=annotate --cov-report=html
else
  coverage_report :=
endif
# directory for coverage html output.
coverage_html_dir := coverage_html

# Name of this package on Pypi
package_name := pywbemtools

# Name of the Python packages for the single tools
cli_package_name := pywbemcli

# Package version (full version, including any pre-release suffixes, e.g. "0.1.0-alpha1")
# Note: Some make actions (such as clobber) cause the package version to change,
# e.g. because the pywbem.egg-info directory or the PKG-INFO file are deleted,
# when a new version tag has been assigned. Therefore, this variable is assigned with
# "=" so that it is evaluated every time it is used.
package_version = $(shell $(PYTHON_CMD) -c "$$(printf 'try:\n from pbr.version import VersionInfo\nexcept ImportError:\n pass\nelse:\n print(VersionInfo(\042$(package_name)\042).release_string())\n')")

# Python full version
python_version := $(shell $(PYTHON_CMD) -c "import sys; sys.stdout.write('%s.%s.%s'%sys.version_info[0:3])")

# Python major version
python_major_version := $(shell $(PYTHON_CMD) -c "import sys; sys.stdout.write('%s'%sys.version_info[0])")

# Python major+minor version for use in file names
python_version_fn := $(shell $(PYTHON_CMD) -c "import sys; sys.stdout.write('%s%s'%(sys.version_info[0],sys.version_info[1]))")

# Directory for the generated distribution files
dist_dir := dist

# Distribution archives (as built by setup.py)
# These variables are set with "=" for the same reason as package_version.
bdist_file = $(dist_dir)/$(package_name)-$(package_version)-py2.py3-none-any.whl
sdist_file = $(dist_dir)/$(package_name)-$(package_version).tar.gz

# Windows installable (as built by setup.py)
win64_dist_file = $(dist_dir)/$(package_name)-$(package_version).win-amd64.exe

# dist_files = $(bdist_file) $(sdist_file) $(win64_dist_file)
dist_files = $(bdist_file) $(sdist_file)

# Directory for generated API documentation
doc_build_dir := build_doc

# Directory where Sphinx conf.py is located
doc_conf_dir := docs

# Documentation generator command
doc_cmd := sphinx-build
doc_opts := -v -d $(doc_build_dir)/doctrees -c $(doc_conf_dir) .

# Dependents for Sphinx documentation build
doc_dependent_files := \
    $(doc_conf_dir)/conf.py \
    $(doc_conf_dir)/pywbemclicmdshelp.rst \
    $(wildcard $(doc_conf_dir)/*.rst) \
    $(wildcard $(doc_conf_dir)/notebooks/*.ipynb) \
    $(wildcard $(cli_package_name)/*.py) \

# Flake8 config file
flake8_rc_file := .flake8

# PyLint config file
pylint_rc_file := .pylintrc

# Source files for check (with PyLint and Flake8)
check_py_files := \
    setup.py \
    $(wildcard $(cli_package_name)/*.py) \
    $(wildcard tests/unit/*.py) \
    $(wildcard $(doc_conf_dir)/notebooks/*.py) \

# Test log
test_log_file := test_$(python_version_fn).log

ifdef TESTCASES
pytest_opts := -k $(TESTCASES)
else
pytest_opts :=
endif

# Files the distribution archive depends upon.
dist_dependent_files := \
    LICENSE \
    README.rst \
    requirements.txt \
    $(wildcard *.py) \
    $(wildcard $(package_name)/*.py) \
    $(wildcard $(cli_package_name)/*.py) \

# No built-in rules needed:
.SUFFIXES:

.PHONY: help
help:
	@echo "Makefile for $(package_name) repository of pywbem project"
	@echo "Package version will be: $(package_version)"
	@echo "Uses the currently active Python environment: Python $(python_version)"
	@echo ""
	@echo "Make targets:"
	@echo "  install    - Install $(package_name) and its Python installation and runtime prereqs"
	@echo "  develop    - install + Install Python development prereqs"
	@echo "  build      - Build the distribution archive files in: $(dist_dir) (requires Linux or OSX)"
	@echo "  buildwin   - Build the Windows installable in: $(dist_dir) (requires Windows 64-bit)"
	@echo "  builddoc   - Build documentation in: $(doc_build_dir)"
	@echo "  check      - Run PyLint and Flake8 on sources and save results in: pylint.log and flake8.log"
	@echo "  test       - Run unit tests (and test coverage) and save results in: $(test_log_file)"
	@echo "               Env.var TESTCASES can be used to specify a py.test expression for its -k option"
	@echo "  all        - Do all of the above (except buildwin when not on Windows)"
	@echo "  uninstall  - Uninstall package from active Python environment"
	@echo "  upload     - build + Upload the distribution archive files to PyPI"
	@echo "  clean      - Remove any temporary files"
	@echo "  clobber    - Remove everything created to ensure clean start"
	@echo ""
	@echo "Environment variables:"
	@echo "  COVERAGE_REPORT - When set, the 'test' target creates a coverage report as"
	@echo "      annotated html files showing lines covered and missed, in the directory:"
	@echo "      $(coverage_html_dir)"
	@echo "      Optional, defaults to no such coverage report."
	@echo "  TESTCASES - When set, 'test' target runs only the specified test cases. The"
	@echo "      value is used for the -k option of pytest (see 'pytest --help')."
	@echo "      Optional, defaults to running all tests."
	@echo "  PACKAGE_LEVEL - Package level to be used for installing dependent Python"
	@echo "      packages in 'install' and 'develop' targets:"
	@echo "        latest - Latest package versions available on Pypi"
	@echo "        minimum - A minimum version as defined in minimum-constraints.txt"
	@echo "      Optional, defaults to 'latest'."
	@echo "  PYTHON_CMD - Python command to be used. Useful for Python 3 in some envs."
	@echo "      Optional, defaults to 'python'."
	@echo "  PIP_CMD - Pip command to be used. Useful for Python 3 in some envs."
	@echo "      Optional, defaults to 'pip'."

.PHONY: _check_version
_check_version:
ifeq (,$(package_version))
	@echo 'Error: Package version could not be determined (requires pbr; run "make install")'
	@false
else
	@true
endif

.PHONY: install
install: install.done
	@echo '$@ done.'

pywbem_os_setup.sh:
	wget -q http://pywbem.readthedocs.io/en/latest/_downloads/pywbem_os_setup.sh
	chmod 755 pywbem_os_setup.sh

pywbem_os_setup.bat:
	wget -q http://pywbem.readthedocs.io/en/latest/_downloads/pywbem_os_setup.bat
	chmod 755 pywbem_os_setup.bat

install_os_pywbem.done: pywbem_os_setup.sh pywbem_os_setup.bat
ifeq ($(PLATFORM),Windows)
	cmd /c pywbem_os_setup.bat install
else
	./pywbem_os_setup.sh install
endif
	touch install_os_pywbem.done
	@echo 'Done: Installed prerequisite OS-level packages for pywbem.'

install.done: install_os_pywbem.done requirements.txt setup.py setup.cfg
	$(PYTHON_CMD) -m pip install $(pip_level_opts) pip setuptools wheel
	$(PIP_CMD) install $(pip_level_opts) -r requirements.txt
	$(PIP_CMD) install $(pip_level_opts) -e .
	$(PYTHON_CMD) -c "import pywbemcli; print('Import: ok')"
	pywbemcli --version
	touch install.done
	@echo 'Done: Installed $(package_name) and its installation and runtime prereqs.'

.PHONY: develop
develop: develop.done
	@echo '$@ done.'

develop.done: install.done dev-requirements.txt
	$(PIP_CMD) install $(pip_level_opts) -r dev-requirements.txt
	touch develop.done
	@echo 'Done: Installed Python development prereqs for $(package_name).'

.PHONY: build
build: $(bdist_file) $(sdist_file)
	@echo '$@ done.'

.PHONY: buildwin
buildwin: $(win64_dist_file)
	@echo '$@ done.'

.PHONY: builddoc
builddoc: html
	@echo '$@ done.'

.PHONY: html
html: $(doc_build_dir)/html/docs/index.html
	@echo '$@ done.'

$(doc_build_dir)/html/docs/index.html: Makefile $(doc_dependent_files)
	rm -fv $@
	$(doc_cmd) -b html $(doc_opts) $(doc_build_dir)/html
	@echo "Done: Created the HTML pages with top level file: $@"

.PHONY: pdf
pdf: Makefile $(doc_dependent_files)
	rm -fv $@
	$(doc_cmd) -b latex $(doc_opts) $(doc_build_dir)/pdf
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(doc_build_dir)/pdf all-pdf
	@echo "Done: Created the PDF files in: $(doc_build_dir)/pdf/"
	@echo '$@ done.'

.PHONY: man
man: Makefile $(doc_dependent_files)
	rm -fv $@
	$(doc_cmd) -b man $(doc_opts) $(doc_build_dir)/man
	@echo "Done: Created the manual pages in: $(doc_build_dir)/man/"
	@echo '$@ done.'

.PHONY: docchanges
docchanges:
	$(doc_cmd) -b changes $(doc_opts) $(doc_build_dir)/changes
	@echo
	@echo "Done: Created the doc changes overview file in: $(doc_build_dir)/changes/"
	@echo '$@ done.'

.PHONY: doclinkcheck
doclinkcheck:
	$(doc_cmd) -b linkcheck $(doc_opts) $(doc_build_dir)/linkcheck
	@echo
	@echo "Done: Look for any errors in the above output or in: $(doc_build_dir)/linkcheck/output.txt"
	@echo '$@ done.'

.PHONY: doccoverage
doccoverage:
	$(doc_cmd) -b coverage $(doc_opts) $(doc_build_dir)/coverage
	@echo "Done: Created the doc coverage results in: $(doc_build_dir)/coverage/python.txt"
	@echo '$@ done.'

.PHONY: check
check: pylint.log flake8.log
	@echo '$@ done.'

.PHONY: flake8
flake8: flake8.log
	@echo '$@ done.'

.PHONY: uninstall
uninstall:
	bash -c '$(PIP_CMD) show $(package_name) >/dev/null; rc=$$?; if [[ $$rc == 0 ]]; then $(PIP_CMD) uninstall -y $(package_name); fi'
	@echo '$@ done.'

.PHONY: test
test: $(test_log_file)
	@echo '$@ done.'

.PHONY: clobber
clobber: uninstall clean
	rm -fv *.done pylint.log flake8.log test_*.log
	rm -Rfv $(doc_build_dir) .tox $(coverage_html_dir)
	rm -fv $(bdist_file) $(sdist_file) $(win64_dist_file)
	@echo 'Done: Removed all build products to get to a fresh state.'
	@echo '$@ done.'

# Also remove any build products that are dependent on the Python version
.PHONY: clean
clean:
	bash -c 'find . -path ./.tox -prune -o -name "*.pyc" -print -o -name "__pycache__" -print -o -name "*.tmp" -print -o -name "tmp_*" -print |xargs -r rm -Rfv'
	rm -fv MANIFEST MANIFEST.in ChangeLog .coverage
	rm -Rfv build .cache $(package_name).egg-info .eggs
	@echo 'Done: Cleaned out all temporary files.'
	@echo '$@ done.'

.PHONY: all
all: install develop build builddoc check test
	@echo '$@ done.'

.PHONY: upload
upload: _check_version uninstall $(dist_files)
ifeq (,$(findstring .dev,$(package_version)))
	@echo '==> This will upload $(package_name) version $(package_version) to PyPI!'
	@echo -n '==> Continue? [yN] '
	@bash -c 'read answer; if [[ "$$answer" != "y" ]]; then echo "Aborted."; false; fi'
	twine upload $(dist_files)
	@echo 'Done: Uploaded $(package_name) version to PyPI: $(package_version)'
	@echo '$@ done.'
else
	@echo 'Error: A development version $(package_version) of $(package_name) cannot be uploaded to PyPI!'
	@false
endif

# Distribution archives.
$(bdist_file) $(sdist_file): _check_version Makefile setup.py $(dist_dependent_files)
	rm -Rfv $(package_name).egg-info .eggs build
	$(PYTHON_CMD) setup.py sdist -d $(dist_dir) bdist_wheel -d $(dist_dir) --universal
	@echo 'Done: Created distribution files: $@'

$(win64_dist_file): _check_version Makefile setup.py $(dist_dependent_files)
ifeq ($(PLATFORM),Windows)
	rm -Rfv $(package_name).egg-info .eggs build
	$(PYTHON_CMD) setup.py bdist_wininst -d $(dist_dir) -o -t "$(package_name) v$(package_version)"
	@echo 'Done: Created Windows installable: $@'
else
	@echo 'Error: Creating Windows installable requires Windows'
	@false
endif

# TODO: Once PyLint has no more errors, remove the dash "-"
pylint.log: Makefile $(pylint_rc_file) $(check_py_files)
ifeq ($(python_major_version), 2)
	rm -fv $@
	-bash -c 'set -o pipefail; pylint --rcfile=$(pylint_rc_file) --output-format=text $(check_py_files) 2>&1 |tee $@.tmp'
	mv -f $@.tmp $@
	@echo 'Done: Created PyLint log file: $@'
else
	@echo 'Info: PyLint requires Python 2; skipping this step on Python $(python_major_version)'
endif

flake8.log: Makefile $(flake8_rc_file) $(check_py_files)
	rm -fv $@
	bash -c 'set -o pipefail; flake8 $(check_py_files) 2>&1 |tee $@.tmp'
	mv -f $@.tmp $@
	@echo 'Done: Created Flake8 log file: $@'

$(test_log_file): Makefile $(cli_package_name)/*.py tests/unit/*.py coveragerc
	rm -fv $@
	bash -c 'set -o pipefail; PYTHONWARNINGS=default py.test --cov $(cli_package_name) $(coverage_report) --cov-config coveragerc $(pytest_opts) --ignore=tools --ignore=tests/live_unit -s 2>&1 |tee $@.tmp'
	mv -f $@.tmp $@
	@echo 'Done: Created test log file: $@'

# update the pywbemclicmdshelp.rst if any file that defines click commands changes.
$(doc_conf_dir)/pywbemclicmdshelp.rst: install.done tools/click_help_capture.py $(cli_package_name)/pywbemcli.py $(cli_package_name)/_cmd*.py
	tools/click_help_capture.py >$@.tmp
	mv -f $@.tmp $@
	@echo 'Done: Created help command info for cmds: $@'
