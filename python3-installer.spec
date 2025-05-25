#
# Conditional build:
%bcond_without	doc		# API documentation
%bcond_without	tests		# unit tests
%bcond_with	bootstrap	# bootsrapping without build and install installed

%if %{with bootstrap}
%undefine	with_doc
%undefine	with_tests
%endif

%define		module	installer
Summary:	A library for installing Python wheels
Summary(pl.UTF-8):	Biblioteka do instalowania pythonowych pakietów wheel
Name:		python3-%{module}
Version:	0.7.0
Release:	5
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.debian.net/installer/%{module}-%{version}.tar.gz
# Source0-md5:	d961d1105c9270049528b1167ed021bc
URL:		https://pypi.org/project/installer/
BuildRequires:	python3-build
BuildRequires:	python3-flit_core >= 3.2.0
BuildRequires:	python3-flit_core < 4
%{!?with_bootstrap:BuildRequires:	python3-installer}
BuildRequires:	python3-modules >= 1:3.7
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-myst_parser
BuildRequires:	python3-sphinx_argparse
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a low-level library for installing a Python package from a
wheel distribution. It provides basic functionality and abstractions
for handling wheels and installing packages from wheels.

%description -l pl.UTF-8
Ten pakiet to niskopoziomowa biblioteka do instalowania pakietów
Pythona dystrybuowanych w formacie wheel. Zapewnia podstawową
funkcjonalność oraz warstwę abstrakcji do obsługi pakietów wheel oraz
instalowania pakietów z plików wheel.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
cd docs
sphinx-build-3 -b html -d _build/doctrees   . _build/html
cd ..
rm -rf docs/_build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with bootstrap}
export PYTHONPATH=$(pwd)/src
%endif
%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTING.md README.md docs/changelog.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
