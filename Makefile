# ------------------------------------------------------------------------------
# Makefile for pybemtools repository of pywbem project
# Based on the Makefile in the pywbem repository of pywbem project
#
# Supported OS platforms for this Makefile:
#     Linux (any distro)
#     OS-X
#     Windows with UNIX-like env such as CygWin (with a UNIX-like shell and
#       Python in the UNIX-like env)
#     native Windows (with the native Windows command processor and Python in
#       Windows)
#
# Prerequisites for running this Makefile:
#   These commands are used on all supported OS platforms. On native Windows,
#   they may be provided by UNIX-like environments such as CygWin:
#     make (GNU make)
#     python (This Makefile uses the active Python environment, virtual Python
#       environments are supported)
#     pip (in the active Python environment)
#   These additional commands are used on Linux, OS-X and on Windows with
#   UNIX-like environments:
#     uname
#     rm, find, xargs, cp
#     The commands listed in pywbem_os_setup.sh
#   These additional commands are used on native Windows:
#     del, copy, rmdir
#     The commands listed in pywbem_os_setup.bat
# ------------------------------------------------------------------------------

# No built-in rules needed:
MAKEFLAGS += --no-builtin-rules
.SUFFIXES:

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
  pip_level_opts := -c minimum-constraints-develop.txt -c minimum-constraints-install.txt
  pip_constraints_deps := minimum-constraints-develop.txt minimum-constraints-install.txt
else
  ifeq ($(PACKAGE_LEVEL),latest)
    pip_level_opts := --upgrade --upgrade-strategy eager
    pip_constraints_deps :=
  else
    $(error Error: Invalid value for PACKAGE_LEVEL variable: $(PACKAGE_LEVEL))
  endif
endif

# Run type (normal, scheduled, release)
ifndef RUN_TYPE
  RUN_TYPE := normal
endif

# Make variables are case sensitive and some native Windows environments have
# ComSpec set instead of COMSPEC.
ifndef COMSPEC
  ifdef ComSpec
    COMSPEC = $(ComSpec)
  endif
endif

# Docker image for end2end tests.
# Keep the version in sync with the test.yml workflow.
ifndef TEST_SERVER_IMAGE
  TEST_SERVER_IMAGE := kschopmeyer/openpegasus-server:0.1.3
endif

# Determine OS platform make runs on.
#
# The PLATFORM variable is set to one of:
# * Windows_native: Windows native environment (the Windows command processor
#   is used as shell and its internal commands are used, such as "del").
# * Windows_UNIX: A UNIX-like envieonment on Windows (the UNIX shell and its
#   internal commands are used, such as "rm").
# * Linux: Some Linux distribution
# * Darwin: OS-X / macOS
#
# This in turn determines the type of shell that is used by make when invoking
# commands, and the set of internal shell commands that is assumed to be
# available (e.g. "del" for the Windows native command processor and "rm" for
# a UNIX-like shell). Note that GNU make always uses the value of the SHELL
# make variable to invoke the shell for its commands, but it does not always
# read that variable from the environment. In fact, the approach GNU make uses
# to set the SHELL make variable is very special, see
# https://www.gnu.org/software/make/manual/html_node/Choosing-the-Shell.html.
# On native Windows this seems to be implemented differently than described:
# SHELL is not set to COMSPEC, so we do that here.
#
# Note: Native Windows and CygWin are hard to distinguish: The native Windows
# envvars are set in CygWin as well. COMSPEC (or ComSpec) is set on both
# platforms. Using "uname" will display CYGWIN_NT-.. on both platforms. If the
# CygWin make is used on native Windows, most of the CygWin behavior is visible
# in context of that make (e.g. a SHELL variable is set, PATH gets converted to
# UNIX syntax, execution of batch files requires execute permission, etc.).
ifeq ($(OS),Windows_NT)
  ifdef PWD
    PLATFORM := Windows_UNIX
  else
    PLATFORM := Windows_native
    ifdef COMSPEC
      SHELL := $(COMSPEC)
    else
      SHELL := cmd.exe
    endif
    .SHELLFLAGS := /c
  endif
else
  # Values: Linux, Darwin
  PLATFORM := $(shell uname -s)
endif

ifeq ($(PLATFORM),Windows_native)
  # Note: The substituted backslashes must be doubled.
  # Remove files (blank-separated list of wildcard path specs)
  RM_FUNC = del /f /q $(subst /,\\,$(1))
  # Remove files recursively (single wildcard path spec)
  RM_R_FUNC = del /f /q /s $(subst /,\\,$(1))
  # Remove directories (blank-separated list of wildcard path specs)
  RMDIR_FUNC = rmdir /q /s $(subst /,\\,$(1))
  # Remove directories recursively (single wildcard path spec)
  RMDIR_R_FUNC = rmdir /q /s $(subst /,\\,$(1))
  # Copy a file, preserving the modified date
  CP_FUNC = copy /y $(subst /,\\,$(1)) $(subst /,\\,$(2))
  ENV = set
  WHICH = where
  DEV_NULL = nul
else
  RM_FUNC = rm -f $(1)
  RM_R_FUNC = find . -type f -name '$(1)' -delete
  RMDIR_FUNC = rm -rf $(1)
  RMDIR_R_FUNC = find . -type d -name '$(1)' | xargs -n 1 rm -rf
  CP_FUNC = cp -r $(1) $(2)
  ENV = env | sort
  WHICH = which -a
  DEV_NULL = /dev/null
endif

# Name of this Python package on Pypi
package_name := pywbemtools

# Names of the commands in the package. The command names are used in
# certain directory names.
command1 := pywbemcli
command2 := pywbemlistener

# Determine if coverage details report generated
# The variable can be passed in as either an environment variable or
# command line variable. When set, generates a set of reports of the
# pywbem/*.py files showing line by line coverage.
ifdef COVERAGE_REPORT
  coverage_report := --cov-report=annotate --cov-report=html
else
  coverage_report :=
endif

# Directory for coverage html output. Must be in sync with the one in .coveragerc.
coverage_html_dir := coverage_html

# Package version (e.g. "1.8.0a1.dev10+gd013028e" during development, or "1.8.0"
# when releasing).
# Note: The package version is automatically calculated by setuptools_scm based
# on the most recent tag in the commit history, increasing the least significant
# version indicator by 1.
# Note: Errors in getting the version (e.g. if setuptools-scm is not installed)
# are detected in _check_version. We avoid confusion by suppressing such errors
# here.
package_version := $(shell $(PYTHON_CMD) -m setuptools_scm 2>$(DEV_NULL))

# The version file is recreated by setuptools-scm on every build, so it is
# excluuded from git, and also from some dependency lists.
version_file := $(package_name)/_version_scm.py

# Python versions
python_version := $(shell $(PYTHON_CMD) tools/python_version.py 3)
python_mn_version := $(shell $(PYTHON_CMD) tools/python_version.py 2)
python_m_version := $(shell $(PYTHON_CMD) tools/python_version.py 1)
pymn := py$(python_mn_version)

# Directory for the generated distribution files
dist_dir := dist

# Distribution archives
# These variables are set with "=" for the same reason as package_version.
bdist_file = $(dist_dir)/$(package_name)-$(package_version)-py3-none-any.whl
sdist_file = $(dist_dir)/$(package_name)-$(package_version).tar.gz

dist_files = $(bdist_file) $(sdist_file)

# Source files in the package
package_py_files := \
    $(wildcard $(package_name)/*.py) \
    $(wildcard $(package_name)/*/*.py) \
		$(wildcard $(package_name)/*/*/*.py) \

doc_help_source_files := \
    $(wildcard $(package_name)/*/_cmd_*.py)

# Directory for generated API documentation
doc_build_dir := build_doc

# Directory where Sphinx conf.py is located
doc_conf_dir := docs

# Paper format for the Sphinx LaTex/PDF builder.
# Valid values: a4, letter
doc_paper_format := a4

# Documentation generator command
doc_cmd := sphinx-build
doc_opts := -v -d $(doc_build_dir)/doctrees -c $(doc_conf_dir) -D latex_elements.papersize=$(doc_paper_format) docs

# File names of automatically generated utility help message text output
doc_utility_help_files := \
    $(doc_conf_dir)/$(command1)/cmdshelp.rst \
    $(doc_conf_dir)/$(command2)/cmdshelp.rst \

# Dependents for Sphinx documentation build
doc_dependent_files := \
    $(doc_conf_dir)/conf.py \
    $(doc_utility_help_files) \
    $(wildcard $(doc_conf_dir)/*.rst) \
    $(wildcard $(doc_conf_dir)/*/*.rst) \
    $(wildcard $(doc_conf_dir)/notebooks/*.ipynb) \
    $(package_py_files) \

# Width for help text display.
# Used for generating the cmdshelp.rst file for each command and for creating
# the help in test cases.
pywbemtools_termwidth := 120

# PYWBEMCLI_ALT_HOME_DIR; Env var defining alternate directory where default
# pywbemcli connection file will be placed for tests rather than the deault '~'
# connection file ane mock caches are placed in this directory.
# This env var value used in pywbemcli/_connection_file_names.py to build these
# filenames with value of directory where pywbemcli files stored during unit
# tests. This is set in this makefile for all tests.
PYWBEMCLI_ALT_HOME_DIR=tmp_tst_pywbemcli_alt_home

# PyLint config file
pylint_rc_file := pylintrc

ifeq ($(PACKAGE_LEVEL),minimum)
  # Using pywbem 0.x
  pylint_ignore := all_types_method_mock_v1old.py,all_types_method_mock_v1new.py,simple_mock_invokemethod_v1old.py,simple_mock_invokemethod_v1new.py,py_err_processatstartup.py
else
  # Using pywbem 1.x
  pylint_ignore := all_types_method_mock_v0.py,simple_mock_invokemethod_v0.py,py_err_processatstartup.py
endif

# PyLint additional options
pylint_opts := --disable=fixme --ignore=$(pylint_ignore)

# Flake8 config file
flake8_rc_file := .flake8

# Safety policy files
safety_install_policy_file := .safety-policy-install.yml
safety_develop_policy_file := .safety-policy-develop.yml

# Python source files to be checked by PyLint and Flake8 and ruff
py_src_files := \
    $(filter-out $(version_file), $(wildcard $(package_name)/*.py)) \
    $(wildcard tests/*.py) \
    $(wildcard tests/*/*.py) \
		$(wildcard tests/*/*/*.py) \
    $(wildcard tests/unit/pywbemcli/testmock/*.py) \
    $(wildcard $(doc_conf_dir)/notebooks/*.py) \

# Python source files with Syntax errors (cannot be suppressed in ruff)
py_err_src_files := \
    $(wildcard tests/unit/pywbemcli/error/*.py) \

# Test log
test_log_file := test_$(python_version_fn).log

ifdef TESTCASES
  pytest_opts := $(TESTOPTS) -k $(TESTCASES)
else
  pytest_opts := $(TESTOPTS)
endif
pytest_end2end_opts := -v --tb=short $(pytest_opts)

pytest_cov_opts := --cov $(package_name) $(coverage_report) --cov-config .coveragerc

pytest_warning_opts := -W default -W ignore::PendingDeprecationWarning
pytest_end2end_warning_opts := $(pytest_warning_opts)

# Files to be put into distribution archive.
# Keep in sync with dist_dependent_files.
# This is used for 'include' statements in MANIFEST.in. The wildcards are used
# as specified, without being expanded.
dist_manifest_in_files := \
    LICENSE.txt \
    README.md \
    README_PYPI.md \
    requirements.txt \
    pyproject.toml \
    $(package_name)/*.py \
    $(package_name)/*/*.py \
    $(package_name)/*/*/*.py \

# Files that are dependents of the distribution archive.
# Keep in sync with dist_manifest_in_files.
dist_dependent_files_all := \
    LICENSE.txt \
    README.md \
    README_PYPI.md \
    requirements.txt \
    pyproject.toml \
    $(wildcard $( package_name)/*.py) \
    $(wildcard $(package_name)/*/*.py) \
    $(wildcard $(package_name)/*/*/*.py) \

# The dependency list actually used, which removes the version file. Reason is that the
# version file is rebuilt during build.
dist_dependent_files := $(filter-out $(version_file), $(dist_dependent_files_all))

# Packages whose dependencies are checked using pip-missing-reqs
check_reqs_packages := pytest coverage coveralls flake8 pylint safety sphinx towncrier

# Scripts are required to install the OS-level components of pywbem.
ifeq ($(PLATFORM),Windows_native)
  pywbem_os_setup_file := pywbem_os_setup.bat
else
  pywbem_os_setup_file := pywbem_os_setup.sh
endif

# This approach for the Pip install command is needed for Windows because
# pip.exe is locked and thus cannot be upgraded. We use this approach also for
# the other packages.
PIP_INSTALL_CMD := $(PYTHON_CMD) -m pip install

ifeq ($(PLATFORM),Windows_native)
  home := $(HOMEDRIVE)$(HOMEPATH)
  cwd := $(shell cd)
else
  home := $(HOME)
  cwd := $(shell pwd)
endif

# Directory for .done files
done_dir := done

.PHONY: help
help:
	@echo "Makefile for $(package_name) package"
	@echo "$(package_name) package version: $(package_version)"
	@echo "Uses the currently active Python environment: Python $(python_version)"
	@echo ""
	@echo "Make targets:"
	@echo "  install    - Install $(package_name) and its installation and runtime prereqs"
	@echo "  develop    - Install $(package_name) development prereqs"
	@echo "  check_reqs - Perform missing dependency checks"
	@echo "  build      - Build the distribution archive files in: $(dist_dir)"
	@echo "  buildwin   - Build the Windows installable in: $(dist_dir) (requires Windows 64-bit)"
	@echo "  builddoc   - Build documentation in: $(doc_build_dir)"
	@echo "  check      - Run Flake8 on sources"
	@echo "  ruff       - Run Ruff (an alternate lint tool) on sources"
	@echo "  pylint     - Run PyLint on sources"
	@echo "  test       - Run unit and function tests"
	@echo "               Env.var TESTCASES can be used to specify a py.test expression for its -k option"
	@echo "  installtest - Run install tests"
	@echo "  safety     - Run Safety for install and all"
	@echo "  end2endtest - Run end2end tests (in tests/end2endtest)"
	@echo "               Env.var TEST_SERVER_IMAGE can be used to specify the Docker image with the WBEM server"
	@echo "  all        - Do all of the above (except buildwin when not on Windows)"
	@echo "  release_branch - Create a release branch when releasing a version (requires VERSION and optionally BRANCH to be set)"
	@echo "  release_publish - Publish to PyPI when releasing a version (requires VERSION and optionally BRANCH to be set)"
	@echo "  start_branch - Create a start branch when starting a new version (requires VERSION and optionally BRANCH to be set)"
	@echo "  start_tag - Create a start tag when starting a new version (requires VERSION and optionally BRANCH to be set)"
	@echo "  todo       - Check for TODOs in Python and docs sources"
	@echo "  clean      - Remove any temporary files"
	@echo "  clobber    - Remove everything created to ensure clean start - use after setting git tag"
	@echo "  pip_list   - Display the Python packages as seen by make"
	@echo "  platform   - Display the information about the platform as seen by make"
	@echo "  env        - Display the environment as seen by make"
	@echo ""
	@echo "Environment variables:"
	@echo "  COVERAGE_REPORT - When non-empty, the 'test' target creates a coverage report as"
	@echo "      annotated html files showing lines covered and missed, in the directory:"
	@echo "      $(coverage_html_dir)"
	@echo "      Optional, defaults to no such coverage report."
	@echo "  TESTCASES - When non-empty, 'test' target runs only the specified test cases. The"
	@echo "      value is used for the -k option of pytest (see 'pytest --help')."
	@echo "      Optional, defaults to running all tests."
	@echo "  TESTOPTS - Optional: Additional options for py.tests (see 'pytest --help')."
	@echo "  TEST_SERVER_IMAGE - Optional: Docker image with target server for end2end tests: $(TEST_SERVER_IMAGE)"
	@echo "  PACKAGE_LEVEL - Package level to be used for installing dependent Python"
	@echo "      packages in 'install' and 'develop' targets:"
	@echo "        latest - Latest package versions available on Pypi"
	@echo "        minimum - A minimum version as defined in minimum-constraints-*.txt"
	@echo "      Optional, defaults to 'latest'."
	@echo "  PYTHON_CMD - Python command to be used. Useful for Python 3 in some envs."
	@echo "      Optional, defaults to 'python'."
	@echo "  PIP_CMD - Pip command to be used. Useful for Python 3 in some envs."
	@echo "      Optional, defaults to 'pip'."
	@echo "  VERSION=... - M.N.U version to be released or started"
	@echo "  BRANCH=... - Name of branch to be released or started (default is derived from VERSION)"

.PHONY: platform
platform:
	@echo "Makefile: Platform related information as seen by make:"
	@echo "Platform: $(PLATFORM)"
	@echo "Home directory: $(home)"
	@echo "Current directory: $(cwd)"
	@echo "Shell used for commands: $(SHELL)"
	@echo "Shell flags: $(.SHELLFLAGS)"
	@echo "Make command location: $(MAKE)"
	@echo "Make version: $(MAKE_VERSION)"
	@echo "Python command name: $(PYTHON_CMD)"
	@echo "Python command location: $(shell $(WHICH) $(PYTHON_CMD))"
	@echo "Python version: $(python_version)"
	@echo "Pip command name: $(PIP_CMD)"
	@echo "Pip command location: $(shell $(WHICH) $(PIP_CMD))"
	@echo "Pip command version: $(shell $(PIP_CMD) --version)"
	@echo "$(package_name) package version: $(package_version)"

.PHONY: pip_list
pip_list:
	@echo "Makefile: Python packages as seen by make:"
	$(PIP_CMD) list

.PHONY: env
env:
	@echo "Makefile: Environment as seen by make:"
	$(ENV)

.PHONY: _check_version
_check_version:
ifeq (,$(package_version))
	$(error Package version could not be determined)
endif

.PHONY: _show_bitsize
_show_bitsize:
	@echo "Makefile: Determining bit size of Python executable"
	$(PYTHON_CMD) tools/python_bitsize.py
	@echo "Makefile: Done determining bit size of Python executable"

# GitHub Actions has Pip 7.1.2 preinstalled on Python 3.4 on Windows, which does
# not support python_requires yet, and thus would update Pip beyond the last
# supported version. This rule ensures we have a minimum version of Pip that
# supports what this project needs.
$(done_dir)/pip_minimum_$(pymn)_$(PACKAGE_LEVEL).done: Makefile minimum-constraints-install.txt
	@echo "Makefile: Upgrading/downgrading Pip to minimum version"
	-$(call RM_FUNC,$@)
	$(PIP_INSTALL_CMD) -c minimum-constraints-install.txt pip
	echo "done" >$@
	@echo "Makefile: Done upgrading/downgrading Pip to minimum version"

# Scripts are required to install the OS-level components of pywbem.
# Makefile gets the required scripts from the pywbem project on GitHub.
pywbem_os_setup.sh: Makefile
	curl -s -o pywbem_os_setup.sh https://raw.githubusercontent.com/pywbem/pywbem/master/pywbem_os_setup.sh
	chmod 755 pywbem_os_setup.sh

pywbem_os_setup.bat: Makefile
	curl -s -o pywbem_os_setup.bat https://raw.githubusercontent.com/pywbem/pywbem/master/pywbem_os_setup.bat

$(done_dir)/install_base_$(pymn)_$(PACKAGE_LEVEL).done: Makefile base-requirements.txt $(pip_constraints_deps)
	@echo "Makefile: Installing/upgrading base Python packages with PACKAGE_LEVEL=$(PACKAGE_LEVEL)"
	-$(call RM_FUNC,$@)
	$(PIP_INSTALL_CMD) $(pip_level_opts) -r base-requirements.txt
	echo "done" >$@
	@echo "Makefile: Done installing/upgrading base Python packages"

$(done_dir)/install_$(package_name)_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/install_base_$(pymn)_$(PACKAGE_LEVEL).done requirements.txt pyproject.toml MANIFEST.in $(pip_constraints_deps)
	@echo "Makefile: Installing $(package_name) (editable) and its Python runtime prerequisites (with PACKAGE_LEVEL=$(PACKAGE_LEVEL))"
	-$(call RM_FUNC,$@)
	-$(call RMDIR_FUNC,build $(package_name).egg-info .eggs)
	$(PIP_INSTALL_CMD) $(pip_level_opts) -r requirements.txt
	$(PIP_INSTALL_CMD) $(pip_level_opts) -e .
	echo "done" >$@
	@echo "Makefile: Done installing $(package_name) and its Python runtime prerequisites"

.PHONY: install
install: $(done_dir)/install_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: Target $@ done."

$(done_dir)/install_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/install_base_$(pymn)_$(PACKAGE_LEVEL).done $(done_dir)/install_$(package_name)_$(pymn)_$(PACKAGE_LEVEL).done
	-$(call RM_FUNC,$@)
	$(PYTHON_CMD) -c "import $(package_name).$(command1)"
	$(PYTHON_CMD) -c "import $(package_name).$(command2)"
	echo "done" >$@

# The following target is supposed to install any prerequisite OS-level packages
# needed for development of pywbemtools. Pywbemtools has no such prerequisite
# packages on its own. However, on Python 3, the 'astroid' package used by
# 'pylint' needs 'typed-ast' which depends on the OS-level packages
# 'libcrypt-devel' and 'python3-devel'. These packages happen to also be used
# by pywbem for development.
$(done_dir)/develop_os_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/install_base_$(pymn)_$(PACKAGE_LEVEL).done $(pywbem_os_setup_file)
	@echo "Makefile: Installing OS-level development requirements"
	-$(call RM_FUNC,$@)
ifeq ($(PLATFORM),Windows_native)
	pywbem_os_setup.bat develop
else
	./pywbem_os_setup.sh develop
endif
	echo "done" >$@
	@echo "Makefile: Done installing OS-level development requirements"

.PHONY: develop
develop: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: Target $@ done."

$(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/install_base_$(pymn)_$(PACKAGE_LEVEL).done $(done_dir)/install_$(pymn)_$(PACKAGE_LEVEL).done $(done_dir)/develop_os_$(pymn)_$(PACKAGE_LEVEL).done dev-requirements.txt $(pip_constraints_deps)
	@echo "Makefile: Installing Python development requirements (with PACKAGE_LEVEL=$(PACKAGE_LEVEL))"
	-$(call RM_FUNC,$@)
	$(PIP_INSTALL_CMD) $(pip_level_opts) -r dev-requirements.txt
	echo "done" >$@
	@echo "Makefile: Done installing Python development requirements"

.PHONY: build
build: $(bdist_file) $(sdist_file)
	@echo "Makefile: Target $@ done."

.PHONY: builddoc
builddoc: html
	@echo "Makefile: Target $@ done."

.PHONY: flake8
flake8: $(done_dir)/flake8_$(pymn)_$(PACKAGE_LEVEL).done
	@echo 'Makefile: Target $@ done.'

.PHONY: check
check: $(done_dir)/flake8_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: Target $@ done."

.PHONY: ruff
ruff: $(done_dir)/ruff_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: Target $@ done."

.PHONY: pylint
pylint: $(done_dir)/pylint_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: Target $@ done."

.PHONY: safety
safety: $(done_dir)/safety_develop_$(pymn)_$(PACKAGE_LEVEL).done $(done_dir)/safety_install_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: Target $@ done."

.PHONY: todo
todo: $(done_dir)/todo_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: Target $@ done."

.PHONY: all
all: install develop check_reqs build builddoc check ruff pylint installtest test
	@echo "Makefile: Target $@ done."

.PHONY: clobber
clobber: clean
	@echo "Makefile: Removing everything for a fresh start"
	-$(call RM_FUNC,*.done epydoc.log $(dist_files) pywbem_os_setup.*)
	-$(call RMDIR_FUNC,$(doc_build_dir) .tox $(coverage_html_dir))
	-$(call RM_R_FUNC,*cover)
	-$(call RM_R_FUNC,*.done)
	@echo "Makefile: Done removing everything for a fresh start"
	@echo "Makefile: Target $@ done."

# Remove *.pyc, __pycache__, MANIFEST, cache, eggs
# Also remove any build products that are dependent on the Python version
.PHONY: clean
clean:
	@echo "Makefile: Removing temporary build products"
	-$(call RM_R_FUNC,*.pyc)
	-$(call RMDIR_R_FUNC,__pycache__)
	-$(call RM_FUNC,MANIFEST)
	-$(call RMDIR_FUNC,build .cache .pytest_cache $(package_name).egg-info .eggs)
	@echo "Makefile: Done removing temporary build products"
	@echo "Makefile: Target $@ done."

.PHONY: release_branch
release_branch:
	@bash -c 'if [ -z "$(VERSION)" ]; then echo ""; echo "Error: VERSION env var is not set"; echo ""; false; fi'
	@bash -c 'if [ -n "$$(git status -s)" ]; then echo ""; echo "Error: Local git repo has uncommitted files:"; echo ""; git status; false; fi'
	git fetch origin
	@bash -c 'if [ -z "$$(git tag -l $(VERSION)a0)" ]; then echo ""; echo "Error: Release start tag $(VERSION)a0 does not exist (the version has not been started)"; echo ""; false; fi'
	@bash -c 'if [ -n "$$(git tag -l $(VERSION))" ]; then echo ""; echo "Error: Release tag $(VERSION) already exists (the version has already been released)"; echo ""; false; fi'
	@bash -c 'if [[ -n "$${BRANCH}" ]]; then echo $${BRANCH} >branch.tmp; elif [[ "$${VERSION#*.*.}" == "0" ]]; then echo "master" >branch.tmp; else echo "stable_$${VERSION%.*}" >branch.tmp; fi'
	@bash -c 'if [ -z "$$(git branch --contains $(VERSION)a0 $$(cat branch.tmp))" ]; then echo ""; echo "Error: Release start tag $(VERSION)a0 is not in target branch $$(cat branch.tmp), but in:"; echo ""; git branch --contains $(VERSION)a0;. false; fi'
	@echo "==> This will start the release of $(package_name) version $(VERSION) to PyPI using target branch $$(cat branch.tmp)"
	@echo -n '==> Continue? [yN] '
	@bash -c 'read answer; if [ "$$answer" != "y" ]; then echo "Aborted."; false; fi'
	bash -c 'git checkout $$(cat branch.tmp)'
	git pull
	@bash -c 'if [ -z "$$(git branch -l release_$(VERSION))" ]; then echo "Creating release branch release_$(VERSION)"; git checkout -b release_$(VERSION); fi'
	git checkout release_$(VERSION)
	make authors
	towncrier build --version $(VERSION) --yes
	@bash -c 'if ls changes/*.rst >/dev/null 2>/dev/null; then echo ""; echo "Error: There are incorrectly named change fragment files that towncrier did not use:"; ls -1 changes/*.rst; echo ""; false; fi'	git commit -asm "Release $(VERSION)"
	git push --set-upstream origin release_$(VERSION)
	rm -f branch.tmp
	@echo "Done: Pushed the release branch to GitHub - now go there and create a PR."
	@echo "Makefile: $@ done."

.PHONY: release_publish
release_publish:
	@bash -c 'if [ -z "$(VERSION)" ]; then echo ""; echo "Error: VERSION env var is not set"; echo ""; false; fi'
	@bash -c 'if [ -n "$$(git status -s)" ]; then echo ""; echo "Error: Local git repo has uncommitted files:"; echo ""; git status; false; fi'
	git fetch origin
	@bash -c 'if [ -n "$$(git tag -l $(VERSION))" ]; then echo ""; echo "Error: Release tag $(VERSION) already exists (the version has already been released)"; echo ""; false; fi'
	@bash -c 'if [[ -n "$${BRANCH}" ]]; then echo $${BRANCH} >branch.tmp; elif [[ "$${VERSION#*.*.}" == "0" ]]; then echo "master" >branch.tmp; else echo "stable_$${VERSION%.*}" >branch.tmp; fi'
	@bash -c 'if [ "$$(git log --format=format:%s origin/$$(cat branch.tmp)~..origin/$$(cat branch.tmp))" != "Release $(VERSION)" ]; then echo ""; echo "Error: Release PR for $(VERSION) has not been merged yet"; echo ""; false; fi'
	@echo "==> This will publish $(package_name) version $(VERSION) to PyPI using target branch $$(cat branch.tmp)"
	@echo -n '==> Continue? [yN] '
	@bash -c 'read answer; if [ "$$answer" != "y" ]; then echo "Aborted."; false; fi'
	bash -c 'git checkout $$(cat branch.tmp)'
	git pull
	git tag -f $(VERSION)
	git push -f --tags
	git branch -D release_$(VERSION)
	git branch -D -r origin/release_$(VERSION)
	rm -f branch.tmp
	@echo "Done: Triggered the publish workflow - now wait for it to finish and verify the publishing."
	@echo "Makefile: $@ done."

.PHONY: start_branch
start_branch:
	@bash -c 'if [ -z "$(VERSION)" ]; then echo ""; echo "Error: VERSION env var is not set"; echo ""; false; fi'
	@bash -c 'if [ -n "$$(git status -s)" ]; then echo ""; echo "Error: Local git repo has uncommitted files:"; echo ""; git status; false; fi'
	git fetch origin
	@bash -c 'if [ -n "$$(git tag -l $(VERSION))" ]; then echo ""; echo "Error: Release tag $(VERSION) already exists (the version has already been released)"; echo ""; false; fi'
	@bash -c 'if [ -n "$$(git tag -l $(VERSION)a0)" ]; then echo ""; echo "Error: Release start tag $(VERSION)a0 already exists (the new version has alreay been started)"; echo ""; false; fi'
	@bash -c 'if [ -n "$$(git branch -l start_$(VERSION))" ]; then echo ""; echo "Error: Start branch start_$(VERSION) already exists (the start of the new version is already underway)"; echo ""; false; fi'
	@bash -c 'if [[ -n "$${BRANCH}" ]]; then echo $${BRANCH} >branch.tmp; elif [[ "$${VERSION#*.*.}" == "0" ]]; then echo "master" >branch.tmp; else echo "stable_$${VERSION%.*}" >branch.tmp; fi'
	@echo "==> This will start new version $(VERSION) using target branch $$(cat branch.tmp)"
	@echo -n '==> Continue? [yN] '
	@bash -c 'read answer; if [ "$$answer" != "y" ]; then echo "Aborted."; false; fi'
	bash -c 'git checkout $$(cat branch.tmp)'
	git pull
	git checkout -b start_$(VERSION)
	echo "Dummy change for starting new version $(VERSION)" >changes/noissue.$(VERSION).notshown.rst
	git add changes/noissue.$(VERSION).notshown.rst
	git commit -asm "Start $(VERSION)"
	git push --set-upstream origin start_$(VERSION)
	rm -f branch.tmp
	@echo "Done: Pushed the start branch to GitHub - now go there and create a PR."
	@echo "Makefile: $@ done."

.PHONY: start_tag
start_tag:
	@bash -c 'if [ -z "$(VERSION)" ]; then echo ""; echo "Error: VERSION env var is not set"; echo ""; false; fi'
	@bash -c 'if [ -n "$$(git status -s)" ]; then echo ""; echo "Error: Local git repo has uncommitted files:"; echo ""; git status; false; fi'
	git fetch origin
	@bash -c 'if [ -n "$$(git tag -l $(VERSION)a0)" ]; then echo ""; echo "Error: Release start tag $(VERSION)a0 already exists (the new version has alreay been started)"; echo ""; false; fi'
	@bash -c 'if [[ -n "$${BRANCH}" ]]; then echo $${BRANCH} >branch.tmp; elif [[ "$${VERSION#*.*.}" == "0" ]]; then echo "master" >branch.tmp; else echo "stable_$${VERSION%.*}" >branch.tmp; fi'
	@bash -c 'if [ "$$(git log --format=format:%s origin/$$(cat branch.tmp)~..origin/$$(cat branch.tmp))" != "Start $(VERSION)" ]; then echo ""; echo "Error: Start PR for $(VERSION) has not been merged yet"; echo ""; false; fi'
	@echo "==> This will complete the start of new version $(VERSION) using target branch $$(cat branch.tmp)"
	@echo -n '==> Continue? [yN] '
	@bash -c 'read answer; if [ "$$answer" != "y" ]; then echo "Aborted."; false; fi'
	bash -c 'git checkout $$(cat branch.tmp)'
	git pull
	git tag -f $(VERSION)a0
	git push -f --tags
	git branch -D start_$(VERSION)
	git branch -D -r origin/start_$(VERSION)
	rm -f branch.tmp
	@echo "Done: Pushed the release start tag and cleaned up the release start branch."
	@echo "Makefile: $@ done."

.PHONY: html
html: $(doc_build_dir)/html/index.html
	@echo "Kakefile: Target $@ done."

$(doc_build_dir)/html/index.html: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done Makefile $(doc_dependent_files)
	@echo "Makefile: Creating the documentation as HTML pages"
	-$(call RM_FUNC,$@)
	$(doc_cmd) -b html $(doc_opts) $(doc_build_dir)/html
	@echo "Makefile: Done creating the documentation as HTML pages; top level file: $@"

.PHONY: pdf
pdf: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done Makefile $(doc_dependent_files)
	@echo "Makefile: Creating the documentation as PDF file"
	-$(call RM_FUNC,$@)
	$(doc_cmd) -b latex $(doc_opts) $(doc_build_dir)/pdf
	@echo "Makefile: Running LaTeX files through pdflatex..."
	$(MAKE) -C $(doc_build_dir)/pdf all-pdf
	@echo "Makefile: Done creating the documentation as PDF file in: $(doc_build_dir)/pdf/"
	@echo "Makefile: Target $@ done."

.PHONY: man
man: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done Makefile $(doc_dependent_files)
	@echo "Makefile: Creating the documentation as man pages"
	-$(call RM_FUNC,$@)
	$(doc_cmd) -b man $(doc_opts) $(doc_build_dir)/man
	@echo "Makefile: Done creating the documentation as man pages in: $(doc_build_dir)/man/"
	@echo "Makefile: Target $@ done."

.PHONY: docchanges
docchanges: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: Creating the doc changes overview file"
	$(doc_cmd) -b changes $(doc_opts) $(doc_build_dir)/changes
	@echo
	@echo "Makefile: Done creating the doc changes overview file in: $(doc_build_dir)/changes/"
	@echo "Makefile: Target $@ done."

.PHONY: doclinkcheck
doclinkcheck: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: Creating the doc link errors file"
	$(doc_cmd) -b linkcheck $(doc_opts) $(doc_build_dir)/linkcheck
	@echo
	@echo "Makefile: Done creating the doc link errors file: $(doc_build_dir)/linkcheck/output.txt"
	@echo "Makefile: Target $@ done."

.PHONY: doccoverage
doccoverage: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: Creating the doc coverage results file"
	$(doc_cmd) -b coverage $(doc_opts) $(doc_build_dir)/coverage
	@echo "Makefile: Done creating the doc coverage results file: $(doc_build_dir)/coverage/python.txt"
	@echo "Makefile: Target $@ done."

# Note: distutils depends on the right files specified in MANIFEST.in, even when
# they are already specified e.g. in 'package_data' in pyproject.toml.
# We generate the MANIFEST.in file automatically, to have a single point of
# control (this Makefile) for what gets into the distribution archive.
MANIFEST.in: Makefile
	@echo "Makefile: Creating the manifest input file"
	echo "# file GENERATED by Makefile, do NOT edit" >$@
ifeq ($(PLATFORM),Windows_native)
	for %%f in ($(dist_manifest_in_files)) do (echo include %%f >>$@)
else
	echo "$(dist_manifest_in_files)" |xargs -n 1 echo include >>$@
endif
	@echo "Makefile: Done creating the manifest input file: $@"

# Distribution archives.
# Note: Deleting MANIFEST causes setuptools to read MANIFEST.in and to
# regenerate MANIFEST. Otherwise, changes in MANIFEST.in will not be used.
# Note: Deleting the 'build' directory is a safeguard against picking up partial
# build products which can lead to incorrect hashbangs in the pywbem scripts in
# wheel archives.
$(sdist_file): pyproject.toml MANIFEST.in $(doc_utility_help_files) $(dist_dependent_files)
	@echo "Makefile: Creating the source distribution archive: $(sdist_file)"
	-$(call RM_FUNC,MANIFEST)
	-$(call RMDIR_FUNC,build $(package_name).egg-info-INFO .eggs)
	$(PYTHON_CMD) -m build --sdist --outdir $(dist_dir) .
	@echo "Makefile: Done creating the source distribution archive: $(sdist_file)"

$(bdist_file) $(version_file): pyproject.toml MANIFEST.in $(doc_utility_help_files) $(dist_dependent_files)
	@echo "Makefile: Creating the normal wheel distribution archive: $(bdist_file)"
	-$(call RM_FUNC,MANIFEST)
	-$(call RMDIR_FUNC,build $(package_name).egg-info-INFO .eggs)
	$(PYTHON_CMD) -m build --wheel --outdir $(dist_dir) -C--universal .
	@echo "Makefile: Done creating the normal wheel distribution archive: $(bdist_file)"

# PyLint status codes:
# * 0 if everything went fine
# * 1 if fatal messages issued
# * 2 if error messages issued
# * 4 if warning messages issued
# * 8 if refactor messages issued
# * 16 if convention messages issued
# * 32 on usage error
# Status 1 to 16 will be bit-ORed.
# The make command checks for statuses: 1,2,32
$(done_dir)/pylint_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done $(pylint_rc_file) $(py_src_files) $(py_err_src_files)
	@echo "Makefile: Running Pylint"
	-$(call RM_FUNC,$@)
	pylint --version
	pylint $(pylint_opts) --rcfile=$(pylint_rc_file) $(py_src_files) $(py_err_src_files)
	echo "done" >$@
	@echo "Makefile: Done running Pylint"

$(done_dir)/flake8_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done $(flake8_rc_file) $(py_src_files) $(py_err_src_files)
	@echo "Makefile: Running Flake8"
	-$(call RM_FUNC,$@)
	flake8 --version
	flake8 --statistics --config=$(flake8_rc_file) --filename='*' $(py_src_files) $(py_err_src_files)
	echo "done" >$@
	@echo "Makefile: Done running Flake8"

$(done_dir)/ruff_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(py_src_files)
	@echo "Makefile: Running Ruff"
	-$(call RM_FUNC,$@)
	ruff --version
	ruff check --unsafe-fixes $(py_src_files)
	echo "done" >$@
	@echo "Makefile: Done running Ruff"

$(done_dir)/safety_develop_$(pymn)_$(PACKAGE_LEVEL).done: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done Makefile $(safety_develop_policy_file) minimum-constraints-develop.txt
	@echo "Makefile: Running Safety for development packages"
	-$(call RM_FUNC,$@)
	bash -c "safety check --policy-file $(safety_develop_policy_file) -r minimum-constraints-develop.txt --full-report || test '$(RUN_TYPE)' != 'release' || exit 1"
	echo "done" >$@
	@echo "Makefile: Done running Safety for development packages"

$(done_dir)/safety_install_$(pymn)_$(PACKAGE_LEVEL).done: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done Makefile $(safety_install_policy_file) minimum-constraints-install.txt
	@echo "Makefile: Running Safety for installation packages"
	-$(call RM_FUNC,$@)
	safety check --policy-file $(safety_install_policy_file) -r minimum-constraints-install.txt --full-report
	echo "done" >$@
	@echo "Makefile: Done running Safety for installation packages"

$(done_dir)/todo_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done $(pylint_rc_file) $(py_src_files)
	@echo "Makefile: Checking for TODOs"
	-$(call RM_FUNC,$@)
	pylint --exit-zero --reports=n --disable=all --enable=fixme $(py_src_files)
	-grep TODO $(doc_conf_dir) -r --include="*.rst"
	echo "done" >$@
	@echo "Makefile: Done checking for TODOs"

.PHONY: check_reqs
check_reqs: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done minimum-constraints-install.txt requirements.txt
	@echo "Makefile: Checking missing dependencies of the package"
	pip-missing-reqs $(package_name) --requirements-file=requirements.txt
	pip-missing-reqs $(package_name) --requirements-file=minimum-constraints-install.txt
	@echo "Makefile: Done checking missing dependencies of the package"
ifeq ($(PLATFORM),Windows_native)
# Reason for skipping on Windows is https://github.com/r1chardj0n3s/pip-check-reqs/issues/67
	@echo "Makefile: Warning: Skipping the checking of missing dependencies of site-packages directory on native Windows" >&2
else
	@echo "Makefile: Checking missing dependencies of some development packages"
	cat minimum-constraints-develop.txt minimum-constraints-install.txt >minimum-constraints-all.txt.tmp
	@rc=0; for pkg in $(check_reqs_packages); do dir=$$($(PYTHON_CMD) -c "import $${pkg} as m,os; dm=os.path.dirname(m.__file__); d=dm if not dm.endswith('site-packages') else m.__file__; print(d)"); cmd="pip-missing-reqs $${dir} --requirements-file=minimum-constraints-all.txt.tmp"; echo $${cmd}; $${cmd}; rc=$$(expr $${rc} + $${?}); done; exit $${rc}
	rm -f minimum-constraints-all.txt.tmp
	@echo "Makefile: Done checking missing dependencies of some development packages"
endif
	@echo "Makefile: $@ done."

.PHONY: test
test: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done $(doc_utility_help_files)
	@echo "Makefile: Running unit and function tests"
ifeq ($(PLATFORM),Windows_native)
	cmd /c "set PYWBEMTOOLS_TERMWIDTH=$(pywbemtools_termwidth) & set PYWBEMCLI_ALT_HOME_DIR=$(PYWBEMCLI_ALT_HOME_DIR) & py.test --color=yes $(pytest_cov_opts) $(pytest_warning_opts) $(pytest_opts) tests/unit -s"
else
	PYWBEMTOOLS_TERMWIDTH=$(pywbemtools_termwidth) PYWBEMCLI_ALT_HOME_DIR=$(PYWBEMCLI_ALT_HOME_DIR) py.test --color=yes $(pytest_cov_opts) $(pytest_warning_opts) $(pytest_opts) tests/unit -s
endif
	@echo "Makefile: Done running tests"

.PHONY: installtest
installtest: $(bdist_file) $(sdist_file) tests/install/test_install.sh
	@echo "Makefile: Running install tests"
ifeq ($(PLATFORM),Windows_native)
	@echo "Makefile: Warning: Skipping install test on native Windows" >&2
else
	tests/install/test_install.sh $(bdist_file) $(sdist_file) $(PYTHON_CMD)
endif
	@echo "Makefile: Done running install tests"

.PHONY: end2endtest
end2endtest: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done
	@echo "Makefile: Running end2end tests"
ifeq ($(PLATFORM),Windows_native)
	cmd /c "set TEST_SERVER_IMAGE=$(TEST_SERVER_IMAGE) & set PYWBEMCLI_ALT_HOME_DIR=$(PYWBEMCLI_ALT_HOME_DIR) & py.test --color=yes $(pytest_end2end_warning_opts) $(pytest_end2end_opts) tests/end2endtest -s"
else
	TEST_SERVER_IMAGE=$(TEST_SERVER_IMAGE) PYWBEMCLI_ALT_HOME_DIR=$(PYWBEMCLI_ALT_HOME_DIR) py.test --color=yes $(pytest_end2end_warning_opts) $(pytest_end2end_opts) tests/end2endtest -s
endif
	@echo "Makefile: Done running end2end tests"

$(doc_conf_dir)/$(command1)/cmdshelp.rst: $(package_name)/$(command1)/$(command1).py $(done_dir)/install_$(pymn)_$(PACKAGE_LEVEL).done tools/click_help_capture.py $(doc_help_source_files)
	@echo "Makefile: Creating $@ for documentation"
ifeq ($(PLATFORM),Windows_native)
	cmd /c "set PYWBEMTOOLS_TERMWIDTH=$(pywbemtools_termwidth) & $(PYTHON_CMD) -u tools/click_help_capture.py $(command1) >$@"
else
	PYWBEMTOOLS_TERMWIDTH=$(pywbemtools_termwidth) $(PYTHON_CMD) -u tools/click_help_capture.py $(command1) >$@
endif
	@echo 'Done: Created help command info for cmds: $@'

$(doc_conf_dir)/$(command2)/cmdshelp.rst: $(package_name)/$(command2)/$(command2).py $(done_dir)/install_$(pymn)_$(PACKAGE_LEVEL).done tools/click_help_capture.py $(doc_help_source_files)
	@echo 'Makefile: Creating $@ for documentation'
ifeq ($(PLATFORM),Windows_native)
	cmd /c "set PYWBEMTOOLS_TERMWIDTH=$(pywbemtools_termwidth) & $(PYTHON_CMD) -u tools/click_help_capture.py $(command2) >$@"
else
	PYWBEMTOOLS_TERMWIDTH=$(pywbemtools_termwidth) $(PYTHON_CMD) -u tools/click_help_capture.py $(command2) >$@
endif
	@echo 'Makefile: Done creating help command info for cmds: $@'
