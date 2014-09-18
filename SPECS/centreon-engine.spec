%define cent_global_prefix  /usr/local/centreon-full/
%define cent_engine_etc     /etc/centreon-engine
%define cent_engine_user    centreon-engine
%define cent_engine_group   centreon-engine

Name:		centreon-engine
Version:	1.4.7
Release:	3%{?dist}
Summary:	Centreon Engine

Group:		Centreon
License:	GPL
URL:		http://centreon.com
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	centreon-clib >= 1.4.0
BuildRequires:  cmake28
BuildRequires:  gcc, gcc-c++
BuildRequires:  zlib-devel, openssl-devel, xerces-c-devel gsoap-devel
Requires:   redhat-lsb-core
Requires:	centreon-clib >= 1.4.0
Requires:   gsoap
Requires:   openssl
Requires:   zlib

%description
Centreon Engine %{version}


%prep
%setup -q


%build
cd build
cmake28 \
    -DWITH_PREFIX=%{cent_global_prefix} \
    -DWITH_PREFIX_CONF=%{cent_engine_etc} \
    -DWITH_USER=%{cent_engine_user} \
    -DWITH_GROUP=%{cent_engine_group} \
    -DWITH_LOGROTATE_SCRIPT=1 \
    -DWITH_VAR_DIR=/var/log/centreon-engine \
    -DWITH_RW_DIR=/var/lib/centreon-engine/rw \
    -DWITH_STARTUP_DIR=/etc/init.d \
    -DWITH_PKGCONFIG_SCRIPT=1 \
    -DWITH_TESTING=0 \
    -DWITH_WEBSERVICE=1 \
    -DWITH_CENTREON_CLIB_INCLUDE_DIR=%{cent_global_prefix}/include \
    -DWITH_CENTREON_CLIB_LIBRARY_DIR=%{cent_global_prefix}/lib .

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd build
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/var/log/centreon-engine
mkdir -p %{buildroot}/var/lib/centreon-engine/rw
rm -rf %{buildroot}%{cent_engine_etc}/*
mkdir %{buildroot}%{cent_global_prefix}/libexec

%clean
rm -rf %{buildroot}

%pre
groupadd %{cent_engine_group} ||:
useradd -g %{cent_engine_group} -m -r -d /var/lib/centreon-engine centreon-engine ||:

%post
chown -R %{cent_engine_user}:%{cent_engine_group} /var/log/centreon-engine
chkconfig centengine on

%preun
service centreon-engine stop ||:
pkill -9 -u %{cent_engine_user} ||:
chkconfig centengine off

%postun
userdel %{cent_engine_user}
groupdel %{cent_engine_group} ||:

%files
%defattr(0660,%{cent_engine_user},%{cent_engine_group},0770)
%dir %{cent_engine_etc}

%attr(0755,root,root) /etc/init.d/centengine

%defattr(0660,%{cent_engine_user},%{cent_engine_group},0770)
/var/log/centreon-engine
/var/lib/centreon-engine
%attr(2770,%{cent_engine_user},%{cent_engine_group}) /var/lib/centreon-engine/rw

%defattr(-,root,root,-)
/etc/logrotate.d/centengine
%{cent_global_prefix}/bin
%{cent_global_prefix}/include/centreon-engine
%{cent_global_prefix}/lib/centreon-engine

%attr(0755,root,root) %dir %{cent_global_prefix}/libexec

%changelog
* Thu Aug 14 2014 Florent Peterschmitt <fpeterschmitt@capensis.fr>
- Init
