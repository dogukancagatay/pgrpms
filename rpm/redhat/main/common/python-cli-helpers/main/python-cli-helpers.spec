%global pypi_name cli_helpers

Summary:	Python helpers for common CLI tasks
Name:		python-cli-helpers
Version:	2.2.1
Release:	1%{?dist}
License:	BSD
URL:		https://github.com/dbcli/cli_helpers
Source0:	https://github.com/dbcli/cli_helpers/archive/refs/tags/v%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python3-configobj python3-devel python3-mock
BuildRequires:	python3-pytest python3-setuptools python3-tabulate
BuildRequires:  python3-terminaltables python3-wcwidth

%global _description\
CLI Helpers is a Python package that makes it easy to perform common\
tasks when building command-line apps. Its a helper library for\
command-line interfaces.
%description %_description

%package -n	python3-cli-helpers
Summary:	%{summary}
%{?python_provide:%python_provide python3-cli-helpers}
Requires:	python3-configobj >= 5.0.5 python3-pygments >= 1.6
Requires:       python3-tabulate >= 0.8.2 python3-terminaltables >= 3.0.0
Requires:       python3-wcwidth

%description -n python3-cli-helpers %_description

%{?python_extras_subpkg:%python_extras_subpkg -n python3-cli-helpers -i %{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info styles}

%prep
%setup -q -n %{pypi_name}-%{version}
%{__rm} -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-cli-helpers
%license LICENSE
%doc AUTHORS CHANGELOG README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Tue Feb 8 2022 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1
- Initial packaging for the PostgreSQL RPM repository to satisfy pgcli dependency.
