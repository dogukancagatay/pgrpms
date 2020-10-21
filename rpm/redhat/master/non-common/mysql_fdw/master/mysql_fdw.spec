%global sname mysql_fdw
%global mysqlfdwmajver 2
%global mysqlfdwmidver 5
%global mysqlfdwminver 5

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	PostgreSQL Foreign Data Wrapper (FDW) for the MySQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{mysqlfdwmajver}.%{mysqlfdwmidver}.%{mysqlfdwminver}
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/REL-%{mysqlfdwmajver}_%{mysqlfdwmidver}_%{mysqlfdwminver}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/EnterpriseDB/mysql_fdw
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros

Requires:	postgresql%{pgmajorversion}-server

%if 0%{?rhel} && 0%{?rhel} <= 6
BuildRequires:	mysql-devel
Requires:	mysql-libs mysql-devel
%else
BuildRequires:	mariadb-devel
Requires:	mariadb-devel
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW) for
the MySQL.

%prep
%setup -q -n %{sname}-REL-%{mysqlfdwmajver}_%{mysqlfdwmidver}_%{mysqlfdwminver}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif

export LDFLAGS="-L%{_libdir}/mysql"

%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%ifarch ppc64 ppc64le
	%{atpath}/sbin/ldconfig
%endif

%postun -p /sbin/ldconfig
%ifarch ppc64 ppc64le
	%{atpath}/sbin/ldconfig
%endif

%files
%defattr(755,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%changelog
* Wed Oct 21 2020 Devrim Gündüz <devrim@gunduz.org> - 2.5.5-1
- Update to 2.5.5

* Mon Aug 3 2020 Devrim Gündüz <devrim@gunduz.org> - 2.5.4-1
- Update to 2.5.4

* Sat Sep 28 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.3-1
- Update to 2.5.3

* Thu Oct 18 2018 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-1
- Update to 2.5.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Mar 13 2018 - Devrim Gündüz <devrim@gunduz.org> 2.4.0-1
- Update to 2.4.0

* Fri Mar 9 2018 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-3
- Add mariadb-devel as Requires, because it supplies versionless
  libmysqlclient.so as dependency.

* Wed Mar 7 2018 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-2
- Add mariadb-libs dependency, per Fahar Abbas.

* Thu Oct 5 2017 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Update to 2.3.0

* Thu Aug 24 2017 - Devrim Gündüz <devrim@gunduz.org> 2.2.0-2
- Attempt to link to mysqlclient available in the OS.

* Tue Jan 17 2017 - Devrim Gündüz <devrim@gunduz.org> 2.2.0-1
- Update to 2.2.0

* Tue Feb 23 2016 - Devrim Gündüz <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2

* Thu Feb 05 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1

* Fri Oct 10 2014 - Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
