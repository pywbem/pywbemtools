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
#     twine (in the active Python environment)
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
  pip_level_opts := -c minimum-constraints.txt
  pip_constraints_deps := minimum-constraints.txt
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
else
  RM_FUNC = rm -f $(1)
  RM_R_FUNC = find . -type f -name '$(1)' -delete
  RMDIR_FUNC = rm -rf $(1)
  RMDIR_R_FUNC = find . -type d -name '$(1)' | xargs -n 1 rm -rf
  CP_FUNC = cp -r $(1) $(2)
  ENV = env | sort
  WHICH = which -a
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

# Package version (full version, including any pre-release suffixes, e.g. "0.1.0-dev1")#
# Note: Some make actions (such as clobber) cause the package version to change,
# e.g. because the pywbem.egg-info directory or the PKG-INFO file are deleted,
# when a new version tag has been assigned. Therefore, this variable is assigned with
# "=" so that it is evaluated every time it is used.
package_version = $(shell $(PYTHON_CMD) setup.py --version)

# Python versions
python_version := $(shell $(PYTHON_CMD) tools/python_version.py 3)
python_mn_version := $(shell $(PYTHON_CMD) tools/python_version.py 2)
python_m_version := $(shell $(PYTHON_CMD) tools/python_version.py 1)
pymn := py$(python_mn_version)

# Directory for the generated distribution files
dist_dir := dist

# Distribution archives
# These variables are set with "=" for the same reason as package_version.
bdist_file = $(dist_dir)/$(package_name)-$(package_version)-py2.py3-none-any.whl
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
safety_all_policy_file := .safety-policy-all.yml

# Python source files to be checked by PyLint and Flake8 and ruff
py_src_files := \
    setup.py \
    $(package_py_files) \
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

ifeq ($(python_mn_version),3.4)
  pytest_cov_opts :=
else
  pytest_cov_opts := --cov $(package_name) $(coverage_report) --cov-config .coveragerc
endif

ifeq ($(python_m_version),3)
  pytest_warning_opts := -W default -W ignore::PendingDeprecationWarning
  pytest_end2end_warning_opts := $(pytest_warning_opts)
else
  pytest_warning_opts := -W default -W ignore::PendingDeprecationWarning
  pytest_end2end_warning_opts := $(pytest_warning_opts)
endif

# Files to be put into distribution archive.
# Keep in sync with dist_dependent_files.
# This is used for 'include' statements in MANIFEST.in. The wildcards are used
# as specified, without being expanded.
dist_manifest_in_files := \
    LICENSE.txt \
    README.md \
    README_PYPI.md \
    requirements.txt \
    *.py \
    $(package_name)/*.py \
    $(package_name)/*/*.py \
    $(package_name)/*/*/*.py \

# Files that are dependents of the distribution archive.
# Keep in sync with dist_manifest_in_files.
dist_dependent_files := \
    LICENSE.txt \
    README.md \
    README_PYPI.md \
    requirements.txt \
    $(wildcard *.py) \
    $(wildcard $( package_name)/*.py) \
    $(wildcard $(package_name)/*/*.py) \
    $(wildcard $(package_name)/*/*/*.py) \

# Packages whose dependencies are checked using pip-missing-reqs
ifeq ($(python_m_version),2)
  check_reqs_packages := pytest coverage coveralls flake8 pylint twine
else
ifeq ($(python_mn_version),3.6)
  check_reqs_packages := pytest coverage coveralls flake8 pylint twine
else
ifeq ($(python_mn_version),3.7)
  check_reqs_packages := pytest coverage coveralls flake8 pylint twine safety
else
  check_reqs_packages := pytest coverage coveralls flake8 pylint twine safety sphinx
endif
endif
endif

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
	@echo "  todo       - Check for TODOs in Python and docs sources"
	@echo "  upload     - build + Upload the distribution archive files to PyPI"
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
	@echo "        minimum - A minimum version as defined in minimum-constraints.txt"
	@echo "      Optional, defaults to 'latest'."
	@echo "  PYTHON_CMD - Python command to be used. Useful for Python 3 in some envs."
	@echo "      Optional, defaults to 'python'."
	@echo "  PIP_CMD - Pip command to be used. Useful for Python 3 in some envs."
	@echo "      Optional, defaults to 'pip'."

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
$(done_dir)/pip_minimum_$(pymn)_$(PACKAGE_LEVEL).done: Makefile minimum-constraints.txt
	@echo "Makefile: Upgrading/downgrading Pip to minimum version"
	-$(call RM_FUNC,$@)
	$(PIP_INSTALL_CMD) -c minimum-constraints.txt pip
	echo "done" >$@
	@echo "Makefile: Done upgrading/downgrading Pip to minimum version"

# Scripts are required to install the OS-level components of pywbem.
# Makefile gets the required scripts from the pywbem project on GitHub.
pywbem_os_setup.sh: Makefile
	curl -s -o pywbem_os_setup.sh https://raw.githubusercontent.com/pywbem/pywbem/master/pywbem_os_setup.sh
	chmod 755 pywbem_os_setup.sh

pywbem_os_setup.bat: Makefile
	curl -s -o pywbem_os_setup.bat https://raw.githubusercontent.com/pywbem/pywbem/master/pywbem_os_setup.bat

$(done_dir)/install_basic_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/pip_minimum_$(pymn)_$(PACKAGE_LEVEL).done $(pip_constraints_deps)
	@echo "Makefile: Installing/upgrading basic Python packages with PACKAGE_LEVEL=$(PACKAGE_LEVEL)"
	-$(call RM_FUNC,$@)
	$(PIP_INSTALL_CMD) $(pip_level_opts) pip setuptools wheel
	echo "done" >$@
	@echo "Makefile: Done installing/upgrading basic Python packages"

$(done_dir)/install_$(package_name)_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/install_basic_$(pymn)_$(PACKAGE_LEVEL).done requirements.txt setup.py MANIFEST.in $(pip_constraints_deps)
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

$(done_dir)/install_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/install_basic_$(pymn)_$(PACKAGE_LEVEL).done $(done_dir)/install_$(package_name)_$(pymn)_$(PACKAGE_LEVEL).done
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
$(done_dir)/develop_os_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/install_basic_$(pymn)_$(PACKAGE_LEVEL).done $(pywbem_os_setup_file)
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

$(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/install_basic_$(pymn)_$(PACKAGE_LEVEL).done $(done_dir)/install_$(pymn)_$(PACKAGE_LEVEL).done $(done_dir)/develop_os_$(pymn)_$(PACKAGE_LEVEL).done dev-requirements.txt $(pip_constraints_deps)
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
safety: $(done_dir)/safety_all_$(pymn)_$(PACKAGE_LEVEL).done $(done_dir)/safety_install_$(pymn)_$(PACKAGE_LEVEL).done
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

.PHONY: upload
upload: _check_version $(dist_files)
	@echo "Makefile: Uploading to PyPI: $(package_name) $(package_version)"
	twine upload $(dist_files)
	@echo "Makefile: Done uploading to PyPI"
	@echo "Makefile: Target $@ done."

.PHONY: html
html: $(doc_build_dir)/html/index.html
	@echo "Kakefile: Target $@ done."

# Boolean variable indicating that Sphinx should be run
# We run Sphinx only on Python>=3.8 because lower Python versions require too old Sphinx versions
run_sphinx := $(shell $(PYTHON_CMD) -c "import sys; py=sys.version_info[0:2]; sys.stdout.write('true' if py>=(3,8) else 'false')")

$(doc_build_dir)/html/index.html: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done Makefile $(doc_dependent_files)
ifeq ($(run_sphinx),true)
	@echo "Makefile: Creating the documentation as HTML pages"
	-$(call RM_FUNC,$@)
	$(doc_cmd) -b html $(doc_opts) $(doc_build_dir)/html
	@echo "Makefile: Done creating the documentation as HTML pages; top level file: $@"
else
	@echo "Skipping Sphinx to create HTML pages on Python version $(python_version)"
endif

.PHONY: pdf
pdf: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done Makefile $(doc_dependent_files)
ifeq ($(run_sphinx),true)
	@echo "Makefile: Creating the documentation as PDF file"
	-$(call RM_FUNC,$@)
	$(doc_cmd) -b latex $(doc_opts) $(doc_build_dir)/pdf
	@echo "Makefile: Running LaTeX files through pdflatex..."
	$(MAKE) -C $(doc_build_dir)/pdf all-pdf
	@echo "Makefile: Done creating the documentation as PDF file in: $(doc_build_dir)/pdf/"
	@echo "Makefile: Target $@ done."
else
	@echo "Skipping Sphinx to create documentation as PDF file on Python version $(python_version)"
endif

.PHONY: man
man: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done Makefile $(doc_dependent_files)
ifeq ($(run_sphinx),true)
	@echo "Makefile: Creating the documentation as man pages"
	-$(call RM_FUNC,$@)
	$(doc_cmd) -b man $(doc_opts) $(doc_build_dir)/man
	@echo "Makefile: Done creating the documentation as man pages in: $(doc_build_dir)/man/"
	@echo "Makefile: Target $@ done."
else
	@echo "Skipping Sphinx to create documentation as man pages on Python version $(python_version)"
endif

.PHONY: docchanges
docchanges: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done
ifeq ($(run_sphinx),true)
	@echo "Makefile: Creating the doc changes overview file"
	$(doc_cmd) -b changes $(doc_opts) $(doc_build_dir)/changes
	@echo
	@echo "Makefile: Done creating the doc changes overview file in: $(doc_build_dir)/changes/"
	@echo "Makefile: Target $@ done."
else
	@echo "Skipping Sphinx to create doc changes overview file on Python version $(python_version)"
endif

.PHONY: doclinkcheck
doclinkcheck: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done
ifeq ($(run_sphinx),true)
	@echo "Makefile: Creating the doc link errors file"
	$(doc_cmd) -b linkcheck $(doc_opts) $(doc_build_dir)/linkcheck
	@echo
	@echo "Makefile: Done creating the doc link errors file: $(doc_build_dir)/linkcheck/output.txt"
	@echo "Makefile: Target $@ done."
else
	@echo "Skipping Sphinx to create doc link errors file on Python version $(python_version)"
endif

.PHONY: doccoverage
doccoverage: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done
ifeq ($(run_sphinx),true)
	@echo "Makefile: Creating the doc coverage results file"
	$(doc_cmd) -b coverage $(doc_opts) $(doc_build_dir)/coverage
	@echo "Makefile: Done creating the doc coverage results file: $(doc_build_dir)/coverage/python.txt"
	@echo "Makefile: Target $@ done."
else
	@echo "Skipping Sphinx to create doc coverage results file on Python version $(python_version)"
endif

# Note: distutils depends on the right files specified in MANIFEST.in, even when
# they are already specified e.g. in 'package_data' in setup.py.
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
# Note: Deleting MANIFEST causes distutils (setup.py) to read MANIFEST.in and to
# regenerate MANIFEST. Otherwise, changes in MANIFEST.in will not be used.
# Note: Deleting build is a safeguard against picking up partial build products
# which can lead to incorrect hashbangs in the pywbem scripts in wheel archives.
$(bdist_file) $(sdist_file): Makefile setup.py MANIFEST.in $(doc_utility_help_files) $(dist_dependent_files)
	@echo "Makefile: Creating the distribution archive files"
	-$(call RM_FUNC,MANIFEST)
	-$(call RMDIR_FUNC,build $(package_name).egg-info-INFO .eggs)
	$(PYTHON_CMD) setup.py sdist -d $(dist_dir) bdist_wheel -d $(dist_dir) --universal
	@echo "Makefile: Done creating the distribution archive files: $(bdist_file) $(sdist_file)"

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
ifeq ($(python_m_version),2)
	@echo "Makefile: Warning: Skipping Pylint on Python $(python_version)" >&2
else
ifeq ($(python_mn_version),3.4)
	@echo "Makefile: Warning: Skipping Pylint on Python $(python_version)" >&2
else
	@echo "Makefile: Running Pylint"
	-$(call RM_FUNC,$@)
	pylint --version
	pylint $(pylint_opts) --rcfile=$(pylint_rc_file) $(py_src_files) $(py_err_src_files)
	echo "done" >$@
	@echo "Makefile: Done running Pylint"
endif
endif

$(done_dir)/flake8_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done $(flake8_rc_file) $(py_src_files) $(py_err_src_files)
	@echo "Makefile: Running Flake8"
	-$(call RM_FUNC,$@)
	flake8 --version
	flake8 --statistics --config=$(flake8_rc_file) --filename='*' $(py_src_files) $(py_err_src_files)
	echo "done" >$@
	@echo "Makefile: Done running Flake8"

$(done_dir)/ruff_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(py_src_files)
ifeq ($(python_mn_version),2.7)
	@echo "Makefile: Warning: Skipping Ruff on Python $(python_version)" >&2
else
ifeq ($(python_mn_version),3.6)
	@echo "Makefile: Warning: Skipping Ruff on Python $(python_version)" >&2
else
	@echo "Makefile: Running Ruff"
	-$(call RM_FUNC,$@)
	ruff --version
	ruff check --unsafe-fixes $(py_src_files)
	echo "done" >$@
	@echo "Makefile: Done running Ruff"
endif
endif

$(done_dir)/safety_all_$(pymn)_$(PACKAGE_LEVEL).done: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done Makefile $(safety_all_policy_file) minimum-constraints.txt minimum-constraints-install.txt
ifeq ($(python_m_version),2)
	@echo "Makefile: Warning: Skipping Safety for all packages on Python $(python_version)" >&2
else
ifeq ($(python_mn_version),3.6)
	@echo "Makefile: Warning: Skipping Safety for all packages on Python $(python_version)" >&2
else
	@echo "Makefile: Running Safety for all packages"
	-$(call RM_FUNC,$@)
	bash -c "safety check --policy-file $(safety_all_policy_file) -r minimum-constraints.txt --full-report || test '$(RUN_TYPE)' != 'release' || exit 1"
	echo "done" >$@
	@echo "Makefile: Done running Safety for all packages"
endif
endif

$(done_dir)/safety_install_$(pymn)_$(PACKAGE_LEVEL).done: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done Makefile $(safety_install_policy_file) minimum-constraints-install.txt
ifeq ($(python_m_version),2)
	@echo "Makefile: Warning: Skipping Safety for install packages on Python $(python_version)" >&2
else
ifeq ($(python_mn_version),3.6)
	@echo "Makefile: Warning: Skipping Safety for install packages on Python $(python_version)" >&2
else
	@echo "Makefile: Running Safety for install packages"
	-$(call RM_FUNC,$@)
	safety check --policy-file $(safety_install_policy_file) -r minimum-constraints-install.txt --full-report
	echo "done" >$@
	@echo "Makefile: Done running Safety for install packages"
endif
endif

$(done_dir)/todo_$(pymn)_$(PACKAGE_LEVEL).done: Makefile $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done $(pylint_rc_file) $(py_src_files)
ifeq ($(python_m_version),2)
	@echo "Makefile: Warning: Skipping checking for TODOs on Python $(python_version)" >&2
else
ifeq ($(python_mn_version),3.4)
	@echo "Makefile: Warning: Skipping checking for TODOs on Python $(python_version)" >&2
else
	@echo "Makefile: Checking for TODOs"
	-$(call RM_FUNC,$@)
	pylint --exit-zero --reports=n --disable=all --enable=fixme $(py_src_files)
	-grep TODO $(doc_conf_dir) -r --include="*.rst"
	echo "done" >$@
	@echo "Makefile: Done checking for TODOs"
endif
endif

.PHONY: check_reqs
check_reqs: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done minimum-constraints.txt requirements.txt
ifeq ($(python_m_version),2)
	@echo "Makefile: Warning: Skipping the checking of missing dependencies on Python $(python_version)" >&2
else
	@echo "Makefile: Checking missing dependencies of the package"
	pip-missing-reqs $(package_name) --requirements-file=requirements.txt
	pip-missing-reqs $(package_name) --requirements-file=minimum-constraints.txt
	@echo "Makefile: Done checking missing dependencies of the package"
ifeq ($(PLATFORM),Windows_native)
# Reason for skipping on Windows is https://github.com/r1chardj0n3s/pip-check-reqs/issues/67
	@echo "Makefile: Warning: Skipping the checking of missing dependencies of site-packages directory on native Windows" >&2
else
	@echo "Makefile: Checking missing dependencies of some development packages"
	@rc=0; for pkg in $(check_reqs_packages); do dir=$$($(PYTHON_CMD) -c "import $${pkg} as m,os; dm=os.path.dirname(m.__file__); d=dm if not dm.endswith('site-packages') else m.__file__; print(d)"); cmd="pip-missing-reqs $${dir} --requirements-file=minimum-constraints.txt"; echo $${cmd}; $${cmd}; rc=$$(expr $${rc} + $${?}); done; exit $${rc}
	@echo "Makefile: Done checking missing dependencies of some development packages"
endif
endif
	@echo "Makefile: $@ done."

.PHONY: test
test: $(done_dir)/develop_$(pymn)_$(PACKAGE_LEVEL).done $(doc_utility_help_files)
	@echo "Makefile: Running unit and function tests"
ifeq ($(PLATFORM),Windows_native)
	cmd /c "set PYWBEMTOOLS_TERMWIDTH=$(pywbemtools_termwidth) & py.test --color=yes $(pytest_cov_opts) $(pytest_warning_opts) $(pytest_opts) tests/unit -s"
else
	PYWBEMTOOLS_TERMWIDTH=$(pywbemtools_termwidth) py.test --color=yes $(pytest_cov_opts) $(pytest_warning_opts) $(pytest_opts) tests/unit -s
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
	cmd /c "set TEST_SERVER_IMAGE=$(TEST_SERVER_IMAGE) & py.test --color=yes $(pytest_end2end_warning_opts) $(pytest_end2end_opts) tests/end2endtest -s"
else
	TEST_SERVER_IMAGE=$(TEST_SERVER_IMAGE) py.test --color=yes $(pytest_end2end_warning_opts) $(pytest_end2end_opts) tests/end2endtest -s
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
