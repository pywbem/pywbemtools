# ------------------------------------------------------------------------------
# Makefile for pybemtools repository of pywbem project
# Based on the makefile in the pywbem repository of pywbem project
#
# Supported OS platforms for this makefile:
#     Linux (any distro)
#     OS-X
#     Windows with UNIX-like env such as CygWin (with a UNIX-like shell and
#       Python in the UNIX-like env)
#     native Windows (with the native Windows command processor and Python in
#       Windows)
#
# Prerequisites for running this makefile:
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
else
  ifeq ($(PACKAGE_LEVEL),latest)
    pip_level_opts := --upgrade --upgrade-strategy eager
  else
    $(error Error: Invalid value for PACKAGE_LEVEL variable: $(PACKAGE_LEVEL))
  endif
endif

# Make variables are case sensitive and some native Windows environments have
# ComSpec set instead of COMSPEC.
ifndef COMSPEC
  ifdef ComSpec
    COMSPEC = $(ComSpec)
  endif
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
  WHICH = which
endif

# Name of this Python package on Pypi
package_name := pywbemtools

# Name of a specific module within the package_name.  This should be a
# subdirectory of the package in git.
# TODO: Future: expand so that multiple modules can reside in the package
module_name := pywbemcli

# Name of the Python package modules
# TODO future: expand so multiple modules are allowed. Right now we have
# one module and directly reference it in the Makefile
pywbemcli_module_path := $(package_name)/$(module_name)

pywbemcli_module_import_name := $(package_name).$(module_name)

# Determine if coverage details report generated
# The variable can be passed in as either an environment variable or
# command line variable. When set, generates a set of reports of the
# pywbem/*.py files showing line by line coverage.
ifdef COVERAGE_REPORT
  coverage_report := --cov-report=annotate --cov-report=html
else
  coverage_report :=
endif

# Directory for coverage html output. Must be in sync with the one in coveragerc.
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

# Source files in the packages
package_py_files := \
    $(wildcard $(package_name)/*.py) \
    $(wildcard $(package_name)/*/*.py) \
		$(wildcard $(package_name)/*/*/*.py) \

doc_help_source_files := \
    $(wildcard $(pywbemcli_module_path)/_cmd_*.py)

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
    $(doc_conf_dir)/pywbemcli/cmdshelp.rst \

# Dependents for Sphinx documentation build
doc_dependent_files := \
    $(doc_conf_dir)/conf.py \
    $(doc_utility_help_files) \
    $(wildcard $(doc_conf_dir)/*.rst) \
    $(wildcard $(doc_conf_dir)/*/*.rst) \
    $(wildcard $(doc_conf_dir)/notebooks/*.ipynb) \
    $(package_py_files) \

# Width for help text display.
# Used for generating docs/pywbemcli/cmdshelp.rst and for creating the help in
# test cases. The expected help in test cases does not exactly need to match
# this width because the comparison removes whitespace.
pywbemcli_termwidth := 120

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

# Python source files to be checked by PyLint and Flake8
py_src_files := \
    setup.py \
    $(package_py_files) \
    $(wildcard tests/*.py) \
    $(wildcard tests/*/*.py) \
    $(wildcard tests/*/*/*.py) \
    $(wildcard tests/*/*/*/*.py) \
    $(wildcard $(doc_conf_dir)/notebooks/*.py) \

# Test log
test_log_file := test_$(python_version_fn).log

# Python source files for test (unit test and function test)
test_src_files := \
    $(wildcard tests/unit/*.py) \
    $(wildcard tests/unit/*/*.py) \
    $(wildcard tests/function/*.py) \

ifdef TESTCASES
  pytest_opts := $(TESTOPTS) -k $(TESTCASES)
else
  pytest_opts := $(TESTOPTS)
endif

ifeq ($(python_m_version),3)
  pytest_warning_opts := -W default -W ignore::PendingDeprecationWarning -W ignore::ResourceWarning
	pytest_end2end_warning_opts := $(pytest_warning_opts)
else
  pytest_warning_opts := -W default -W ignore::PendingDeprecationWarning
  pytest_end2end_warning_opts := $(pytest_warning_opts)
endif

ifeq ($(python_mn_version),3.4)
  pytest_cov_opts :=
else
  pytest_cov_opts := --cov $(pywbemcli_module_path) $(coverage_report) --cov-config coveragerc
endif

# Files to be put into distribution archive.
# Keep in sync with dist_dependent_files.
# This is used for 'include' statements in MANIFEST.in. The wildcards are used
# as specified, without being expanded.
dist_manifest_in_files := \
    LICENSE.txt \
    README.rst \
		README_PYPI.rst \
		requirements.txt \
    *.py \
    $(package_name)/*.py \
    $(package_name)/*/*.py \
		$(package_name)/*/*/*.py \

# Files that are dependents of the distribution archive.
# Keep in sync with dist_manifest_in_files.
dist_dependent_files := \
    LICENSE.txt \
    README.rst \
		README_PYPI.rst \
		requirements.txt \
    $(wildcard *.py) \
    $(wildcard $(package_name)/*.py) \
    $(wildcard $(package_name)/*/*.py) \
		$(wildcard $(package_name)/*/*/*.py) \

# Scripts are required to install the OS-level components of pywbem.
ifeq ($(PLATFORM),Windows_native)
  pywbem_os_setup_file := pywbem_os_setup.bat
else
  pywbem_os_setup_file := pywbem_os_setup.sh
endif

PIP_INSTALL_CMD := $(PYTHON_CMD) -m pip install

.PHONY: help
help:
	@echo "Makefile for $(package_name) package"
	@echo "$(package_name) package version: $(package_version)"
	@echo "Uses the currently active Python environment: Python $(python_version)"
	@echo ""
	@echo "Make targets:"
	@echo "  install    - Install $(package_name) and its installation and runtime prereqs"
	@echo "  develop    - Install $(package_name) development prereqs"
	@echo "  build      - Build the distribution archive files in: $(dist_dir)"
	@echo "  buildwin   - Build the Windows installable in: $(dist_dir) (requires Windows 64-bit)"
	@echo "  builddoc   - Build documentation in: $(doc_build_dir)"
	@echo "  check      - Run PyLint and Flake8 on sources and save results in: pylint.log and flake8.log"
	@echo "  pylint     - Run PyLint on sources"
	@echo "  test       - Run unit and function tests"
	@echo "               Env.var TESTCASES can be used to specify a py.test expression for its -k option"
	@echo "  installtest - Run install tests"
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
	@echo "makefile: Platform related information as seen by make:"
	@echo "Platform: $(PLATFORM)"
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
	@echo "makefile: Python packages as seen by make:"
	$(PIP_CMD) list

.PHONY: env
env:
	@echo "Environment as seen by make:"
	$(ENV)

.PHONY: _check_version
_check_version:
ifeq (,$(package_version))
	$(error Package version could not be determined)
endif

pip_upgrade_$(pymn).done: Makefile
	-$(call RM_FUNC,$@)
	$(PYTHON_CMD) -m pip install $(pip_level_opts) pip
	echo "done" >$@

install_basic_$(pymn).done: Makefile pip_upgrade_$(pymn).done
	@echo "makefile: Installing/upgrading basic Python packages with PACKAGE_LEVEL=$(PACKAGE_LEVEL)"
	-$(call RM_FUNC,$@)
	$(PYTHON_CMD) remove_duplicate_setuptools.py
# Keep the condition for the 'wheel' package consistent with the requirements & constraints files.
# The approach with "python -m pip" is needed for Windows because pip.exe may be locked.
	$(PIP_INSTALL_CMD) $(pip_level_opts) setuptools wheel
	echo "done" >$@
	@echo "makefile: Done installing/upgrading basic Python packages"

# Scripts are required to install the OS-level components of pywbem.
# Makefile gets the required scripts from the pywbem project on GitHub.
pywbem_os_setup.sh:
	wget -q -O pywbem_os_setup.sh https://raw.githubusercontent.com/pywbem/pywbem/master/pywbem_os_setup.sh
	chmod 755 pywbem_os_setup.sh

pywbem_os_setup.bat:
	wget -q -O pywbem_os_setup.bat https://raw.githubusercontent.com/pywbem/pywbem/master/pywbem_os_setup.bat

.PHONY: install_os
install_os: install_os_$(pymn).done
	@echo "makefile: Target $@ done."

install_os_$(pymn).done: Makefile pip_upgrade_$(pymn).done $(pywbem_os_setup_file)
	@echo "makefile: Installing OS-level installation and runtime requirements"
	-$(call RM_FUNC,$@)
ifeq ($(PLATFORM),Windows_native)
	pywbem_os_setup.bat install
else
	./pywbem_os_setup.sh install
endif
	echo "done" >$@
	@echo "makefile: Done installing OS-level installation and runtime requirements"

.PHONY: _show_bitsize
_show_bitsize:
	@echo "makefile: Determining bit size of Python executable"
	$(PYTHON_CMD) tools/python_bitsize.py
	@echo "makefile: Done determining bit size of Python executable"

install_$(package_name)_$(pymn).done: Makefile pip_upgrade_$(pymn).done requirements.txt setup.py MANIFEST.in
	@echo "makefile: Installing $(package_name) (editable) and its Python runtime prerequisites (with PACKAGE_LEVEL=$(PACKAGE_LEVEL))"
	-$(call RM_FUNC,$@)
	-$(call RMDIR_FUNC,build $(package_name).egg-info .eggs)
	$(PIP_INSTALL_CMD) $(pip_level_opts) -r requirements.txt
	$(PIP_INSTALL_CMD) $(pip_level_opts) -e .
	echo "done" >$@
	@echo "makefile: Done installing $(package_name) and its Python runtime prerequisites"

.PHONY: install
install: install_$(pymn).done
	@echo "makefile: Target $@ done."

install_$(pymn).done: Makefile install_os_$(pymn).done install_basic_$(pymn).done install_$(package_name)_$(pymn).done
	-$(call RM_FUNC,$@)
	$(PYTHON_CMD) -c "import $(pywbemcli_module_import_name)"
	echo "done" >$@

.PHONY: develop_os
develop_os: develop_os_$(pymn).done
	@echo "makefile: Target $@ done."

# The following target is supposed to install any prerequisite OS-level packages
# needed for development of pywbemtools. Pywbemtools has no such prerequisite
# packages on its own. However, on Python 3, the 'astroid' package used by
# 'pylint' needs 'typed-ast' which depends on the OS-level packages
# 'libcrypt-devel' and 'python3-devel'. These packages happen to also be used
# by pywbem for development.
develop_os_$(pymn).done: Makefile pip_upgrade_$(pymn).done $(pywbem_os_setup_file)
	@echo "makefile: Installing OS-level development requirements"
	-$(call RM_FUNC,$@)
ifeq ($(PLATFORM),Windows_native)
	pywbem_os_setup.bat develop
else
	./pywbem_os_setup.sh develop
endif
	echo "done" >$@
	@echo "makefile: Done installing OS-level development requirements"

.PHONY: develop
develop: develop_$(pymn).done
	@echo "makefile: Target $@ done."

develop_$(pymn).done: pip_upgrade_$(pymn).done install_$(pymn).done develop_os_$(pymn).done install_basic_$(pymn).done dev-requirements.txt
	@echo "makefile: Installing Python development requirements (with PACKAGE_LEVEL=$(PACKAGE_LEVEL))"
	-$(call RM_FUNC,$@)
	$(PIP_INSTALL_CMD) $(pip_level_opts) -r dev-requirements.txt
	echo "done" >$@
	@echo "makefile: Done installing Python development requirements"

.PHONY: build
build: $(bdist_file) $(sdist_file)
	@echo "makefile: Target $@ done."

.PHONY: builddoc
builddoc: html
	@echo "makefile: Target $@ done."

.PHONY: flake8
flake8: flake8_$(pymn).done
	@echo '$@ done.'

.PHONY: check
check: flake8_$(pymn).done safety_$(pymn).done
	@echo "makefile: Target $@ done."

.PHONY: pylint
pylint: pylint_$(pymn).done
	@echo "makefile: Target $@ done."

.PHONY: todo
todo: todo_$(pymn).done
	@echo "makefile: Target $@ done."

.PHONY: all
all: install develop build builddoc check pylint installtest test
	@echo "makefile: Target $@ done."

.PHONY: clobber
clobber: clean
	@echo "makefile: Removing everything for a fresh start"
	-$(call RM_FUNC,*.done epydoc.log $(dist_files) $(pywbemcli_module_path)/*cover pywbem_os_setup.*)
	-$(call RMDIR_FUNC,$(doc_build_dir) .tox $(coverage_html_dir))
	@echo "makefile: Done removing everything for a fresh start"
	@echo "makefile: Target $@ done."

# Remove *.pyc, __pycache__, MANIFEST, cache, eggs
# Also remove any build products that are dependent on the Python version
.PHONY: clean
clean:
	@echo "makefile: Removing temporary build products"
	-$(call RM_R_FUNC,*.pyc)
	-$(call RMDIR_R_FUNC,__pycache__)
	-$(call RM_FUNC,MANIFEST)
	-$(call RMDIR_FUNC,build .cache .pytest_cache $(package_name).egg-info .eggs)
	@echo "makefile: Done removing temporary build products"
	@echo "makefile: Target $@ done."

.PHONY: upload
upload: _check_version $(dist_files)
	@echo "makefile: Uploading to PyPI: $(package_name) $(package_version)"
	twine upload $(dist_files)
	@echo "makefile: Done uploading to PyPI"
	@echo "makefile: Target $@ done."

.PHONY: html
html: $(doc_build_dir)/html/index.html
	@echo "makefile: Target $@ done."

$(doc_build_dir)/html/index.html: develop_$(pymn).done Makefile $(doc_dependent_files)
	@echo "makefile: Creating the documentation as HTML pages"
	-$(call RM_FUNC,$@)
	$(doc_cmd) -b html $(doc_opts) $(doc_build_dir)/html
	@echo "makefile: Done creating the documentation as HTML pages; top level file: $@"

.PHONY: pdf
pdf: develop_$(pymn).done Makefile $(doc_dependent_files)
	@echo "makefile: Creating the documentation as PDF file"
	-$(call RM_FUNC,$@)
	$(doc_cmd) -b latex $(doc_opts) $(doc_build_dir)/pdf
	@echo "makefile: Running LaTeX files through pdflatex..."
	$(MAKE) -C $(doc_build_dir)/pdf all-pdf
	@echo "makefile: Done creating the documentation as PDF file in: $(doc_build_dir)/pdf/"
	@echo "makefile: Target $@ done."

.PHONY: man
man: develop_$(pymn).done Makefile $(doc_dependent_files)
	@echo "Makefile: Creating the documentation as man pages"
	-$(call RM_FUNC,$@)
	$(doc_cmd) -b man $(doc_opts) $(doc_build_dir)/man
	@echo "makefile: Done creating the documentation as man pages in: $(doc_build_dir)/man/"
	@echo "makefile: Target $@ done."

.PHONY: docchanges
docchanges: develop_$(pymn).done
	@echo "makefile: Creating the doc changes overview file"
	$(doc_cmd) -b changes $(doc_opts) $(doc_build_dir)/changes
	@echo
	@echo "makefile: Done creating the doc changes overview file in: $(doc_build_dir)/changes/"
	@echo "makefile: Target $@ done."

.PHONY: doclinkcheck
doclinkcheck: develop_$(pymn).done
	@echo "makefile: Creating the doc link errors file"
	$(doc_cmd) -b linkcheck $(doc_opts) $(doc_build_dir)/linkcheck
	@echo
	@echo "makefile: Done creating the doc link errors file: $(doc_build_dir)/linkcheck/output.txt"
	@echo "makefile: Target $@ done."

.PHONY: doccoverage
doccoverage: develop_$(pymn).done
	@echo "makefile: Creating the doc coverage results file"
	$(doc_cmd) -b coverage $(doc_opts) $(doc_build_dir)/coverage
	@echo "makefile: Done creating the doc coverage results file: $(doc_build_dir)/coverage/python.txt"
	@echo "makefile: Target $@ done."

# Note: distutils depends on the right files specified in MANIFEST.in, even when
# they are already specified e.g. in 'package_data' in setup.py.
# We generate the MANIFEST.in file automatically, to have a single point of
# control (this Makefile) for what gets into the distribution archive.
MANIFEST.in: Makefile $(dist_manifest_in_files)
	@echo "makefile: Creating the manifest input file"
	echo "# file GENERATED by Makefile, do NOT edit" >$@
ifeq ($(PLATFORM),Windows_native)
	for %%f in ($(dist_manifest_in_files)) do (echo include %%f >>$@)
else
	echo "$(dist_manifest_in_files)" |xargs -n 1 echo include >>$@
endif
	@echo "makefile: Done creating the manifest input file: $@"

# Distribution archives.
# Note: Deleting MANIFEST causes distutils (setup.py) to read MANIFEST.in and to
# regenerate MANIFEST. Otherwise, changes in MANIFEST.in will not be used.
# Note: Deleting build is a safeguard against picking up partial build products
# which can lead to incorrect hashbangs in the pywbem scripts in wheel archives.
$(bdist_file) $(sdist_file): _check_version setup.py MANIFEST.in $(doc_utility_help_files) $(dist_dependent_files)
	@echo "makefile: Creating the distribution archive files"
	-$(call RM_FUNC,MANIFEST)
	-$(call RMDIR_FUNC,build $(package_name).egg-info-INFO .eggs)
	$(PYTHON_CMD) setup.py sdist -d $(dist_dir) bdist_wheel -d $(dist_dir) --universal
	@echo "makefile: Done creating the distribution archive files: $(bdist_file) $(sdist_file)"

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
pylint_$(pymn).done: develop_$(pymn).done Makefile $(pylint_rc_file) $(py_src_files)
ifeq ($(python_m_version),2)
	@echo "makefile: Warning: Skipping Pylint on Python $(python_version)" >&2
else
ifeq ($(python_mn_version),3.4)
	@echo "makefile: Warning: Skipping Pylint on Python $(python_version)" >&2
else
	@echo "makefile: Running Pylint"
	-$(call RM_FUNC,$@)
	pylint --version
	pylint $(pylint_opts) --rcfile=$(pylint_rc_file) $(py_src_files)
	echo "done" >$@
	@echo "makefile: Done running Pylint"
endif
endif

flake8_$(pymn).done: develop_$(pymn).done Makefile $(flake8_rc_file) $(py_src_files)
	@echo "makefile: Running Flake8"
	-$(call RM_FUNC,$@)
	flake8 --version
	flake8 --statistics --config=$(flake8_rc_file) --filename='*' $(py_src_files)
	echo "done" >$@
	@echo "makefile: Done running Flake8"

safety_$(pymn).done: develop_$(pymn).done Makefile minimum-constraints.txt
	@echo "makefile: Running pyup.io safety check"
	-$(call RM_FUNC,$@)
	-safety check -r minimum-constraints.txt --full-report
	echo "done" >$@
	@echo "makefile: Done running pyup.io safety check"

todo_$(pymn).done: develop_$(pymn).done Makefile $(pylint_rc_file) $(py_src_files)
ifeq ($(python_m_version),2)
	@echo "makefile: Warning: Skipping checking for TODOs on Python $(python_version)" >&2
else
ifeq ($(python_mn_version),3.4)
	@echo "makefile: Warning: Skipping checking for TODOs on Python $(python_version)" >&2
else
	@echo "makefile: Checking for TODOs"
	-$(call RM_FUNC,$@)
	pylint --exit-zero --reports=n --disable=all --enable=fixme $(py_src_files)
	-grep TODO $(doc_conf_dir) -r --include="*.rst"
	echo "done" >$@
	@echo "makefile: Done checking for TODOs"
endif
endif

.PHONY: test
test: develop_$(pymn).done $(doc_utility_help_files)
	@echo "makefile: Running unit and function tests"
ifeq ($(PLATFORM),Windows_native)
	cmd /c "set PYWBEMCLI_TERMWIDTH=$(pywbemcli_termwidth) & set PYWBEMCLI_DEPRECATION_WARNINGS=false& py.test --color=yes $(pytest_cov_opts) $(pytest_warning_opts) $(pytest_opts) tests/unit -s"
else
	PYWBEMCLI_TERMWIDTH=$(pywbemcli_termwidth) PYWBEMCLI_DEPRECATION_WARNINGS=false py.test --color=yes $(pytest_cov_opts) $(pytest_warning_opts) $(pytest_opts) tests/unit -s
endif
	@echo "makefile: Done running tests"

.PHONY: installtest
installtest: $(bdist_file) $(sdist_file) tests/install/test_install.sh
	@echo "makefile: Running install tests"
ifeq ($(PLATFORM),Windows_native)
	@echo "makefile: Warning: Skipping install test on native Windows" >&2
else
	tests/install/test_install.sh $(bdist_file) $(sdist_file) $(PYTHON_CMD)
endif
	@echo "makefile: Done running install tests"

# update the pywbemcli/cmdshelp.rst if any file that defines click commands changes.
$(doc_conf_dir)/pywbemcli/cmdshelp.rst: install_$(pymn).done tools/click_help_capture.py $(pywbemcli_module_path)/pywbemcli.py $(doc_help_source_files)
	@echo 'makefile: Creating $@ for documentation'
ifeq ($(PLATFORM),Windows_native)
	cmd /c "set PYWBEMCLI_TERMWIDTH=$(pywbemcli_termwidth) & $(PYTHON_CMD) -u tools/click_help_capture.py >$@.tmp"
else
	PYWBEMCLI_TERMWIDTH=$(pywbemcli_termwidth) $(PYTHON_CMD) -u tools/click_help_capture.py >$@.tmp
endif
	-$(call RM_FUNC,$@)
	-$(call CP_FUNC,$@.tmp,$@)
	-$(call RM_FUNC,$@.tmp)
	@echo 'Done: Created help command info for cmds: $@'
