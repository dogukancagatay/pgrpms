%global pgmajorversion 92
%global pginstdir /usr/pgsql-9.2
%global sname pg_partman

Summary:	A PostgreSQL extension to manage partitioned tables by time or ID
Name:		%{sname}%{pgmajorversion}
Version:	1.8.2
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		Makefile-pgxs.patch
URL:		http://pgxn.org/dist/pg_partman/
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server, python-psycopg2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pg_partman is a PostgreSQL extension to manage partitioned tables by time or ID.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README and howto file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/extension
install -m 644 README.md  %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
install -m 644 doc/pg_partman.md  %{buildroot}%{pginstdir}/share/extension/
install -m 644 doc/howto.md %{buildroot}%{pginstdir}/share/extension/%{sname}-howto.md
rm -f %{buildroot}%{_docdir}/pgsql/extension/pg_partman.md
rm -f %{buildroot}%{_docdir}/pgsql/extension/howto.md

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}.md
%doc %{pginstdir}/share/extension/%{sname}.md
%doc %{pginstdir}/share/extension/%{sname}-howto.md
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%ghost %{pginstdir}/bin/*.pyo
%ghost %{pginstdir}/bin/*.pyc
%attr(755, root, -) %{pginstdir}/bin/check_unique_constraint.py
%attr(755, root, -) %{pginstdir}/bin/reapply_constraints.py
%attr(755, root, -) %{pginstdir}/bin/reapply_foreign_keys.py
%attr(755, root, -) %{pginstdir}/bin/dump_partition.py
%attr(755, root, -) %{pginstdir}/bin/partition_data.py
%attr(755, root, -) %{pginstdir}/bin/reapply_indexes.py
%attr(755, root, -) %{pginstdir}/bin/undo_partition.py

%changelog
* Sat Mar 7 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.8.2-1
- Update to 1.8.2

* Wed Feb 25 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.8.0-1
- Update to 1.8.0
- Remove executable bit from docs

* Wed Jun 18 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.7.2-1
- Update to 1.7.2

* Tue Apr 29 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.7.0-1
- Update to 1.7.0

* Thu Mar 6 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.6.1-1
- Update to 1.6.1

* Sat Feb 15 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.6.0-1
- Update to 1.6.0

* Wed Jan 15 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.5.1-1
- Update to 1.5.1

* Thu Oct 31 2013 - Devrim GUNDUZ <devrim@gunduz.org> 1.4.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
