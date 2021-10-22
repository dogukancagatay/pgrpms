%global sname	pgmoneta

Name:		%{sname}
Version:	0.5.3
Release:	1%{dist}
Summary:	Backup / restore for PostgreSQL
License:	BSD
URL:		https://github.com/%{sname}/%{sname}
Source0:	https://github.com/%{sname}/%{sname}/archive/%{version}.tar.gz
Source1:	%{sname}.service
Source2:	%{sname}-tmpfiles.d

Patch0:		%{sname}-conf-rpm.patch
BuildRequires:	gcc cmake make python3-docutils zlib-devel libzstd-devel
BuildRequires:	libev libev-devel openssl openssl-devel systemd systemd-devel
Requires:	libev openssl systemd postgresql zlib libzstd

# Systemd stuff
BuildRequires:		systemd, systemd-devel
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires(post):		systemd-sysvinit
%endif
%else
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif

Obsoletes:	%{sname}_13 < 0.2.0-2

%description
pgmoneta is a backup / restore solution for PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build

%{__mkdir} build
cd build
cmake -DCMAKE_BUILD_TYPE=Release .. -DCMAKE_INSTALL_PREFIX=/usr
%{__make}

%install
cd build
%{__make} install DESTDIR=%{buildroot}

%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{sname}
%{__mv} %{buildroot}/usr/etc/%{sname}/%{sname}.conf %{buildroot}%{_sysconfdir}/%{sname}

%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{sname}.service

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE2} %{buildroot}/%{_tmpfilesdir}/%{sname}.conf

%post
%{__chown} -R postgres:postgres %{_sysconfdir}/%{sname}
%{__mkdir} -p /var/log/%{sname}
%{__chown} -R postgres:postgres /var/log/%{sname}
if [ $1 -eq 1 ] ; then
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version}
    %if 0%{?suse_version} >= 1315
     %service_add_pre %{same}.service
    %endif
   %else
    %systemd_post %{sname}.service
    %endif
fi


%preun
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{sname}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{sname}.service >/dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ] ; then
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %{sname}.service >/dev/null 2>&1 || :
fi

%files
%license LICENSE
%{_bindir}/%{sname}
%{_bindir}/%{sname}-admin
%{_bindir}/%{sname}-cli
%config %{_sysconfdir}/%{sname}/%{sname}.conf
%{_libdir}/libpgmoneta.so*
%dir %{_docdir}/%{sname}
%{_docdir}/%{sname}/*
%{_mandir}/man1/%{sname}*
%{_mandir}/man5/%{sname}*
%{_tmpfilesdir}/%{sname}.conf
%{_unitdir}/%{sname}.service

%changelog
* Fri Oct 22 2021 Devrim Gündüz <devrim@gunduz.org> 0.5.3-1
- Update to 0.5.3

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> 0.5.2-1
- Update to 0.5.2

* Thu Sep 23 2021 Devrim Gündüz <devrim@gunduz.org> 0.5.1-1
- Update to 0.5.1

* Wed Sep 1 2021 Devrim Gündüz <devrim@gunduz.org> 0.5.0-2
- Add systemd support (unit file and tmpfiles.d support)
- Create log directory

* Thu Aug 26 2021 Devrim Gündüz <devrim@gunduz.org> 0.5.0-1
- Update to 0.5.0

* Thu Aug 12 2021 Devrim Gündüz <devrim@gunduz.org> 0.4.0-1
- Update to 0.4.0

* Tue Jul 20 2021 Devrim Gündüz <devrim@gunduz.org> 0.3.1-1
- Update to 0.3.1

* Sun Jul 4 2021 Devrim Gündüz <devrim@gunduz.org> 0.3.0-1
- Update to 0.3.0

* Thu Jun 17 2021 Devrim Gündüz <devrim@gunduz.org> 0.2.0-2
- Remove PostgreSQL version number from the package. This
  is a common one.

* Mon Jun 14 2021 Devrim Gündüz <devrim@gunduz.org> 0.2.0-1
- Update to 0.2.0

* Fri May 28 2021 Devrim Gündüz <devrim@gunduz.org> 0.1.0-1
- Initial packaging for PostgreSQL RPM repository. Took spec
  file from upstream.
