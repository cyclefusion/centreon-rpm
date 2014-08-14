%define cent_global_prefix  /usr/local/centreon-full/
%define cent_broker_etc     /etc/centreon-broker
%define cent_broker_user    centreon-broker
%define cent_broker_group   centreon-broker

Name:		centreon-broker
Version:	2.6.2
Release:	1%{?dist}
Summary:	Centreon Broker

Group:		Centreon
License:	GPL
URL:		http://centreon.com
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	cmake28
BuildRequires:  qt-devel >= 4.7.4
BuildRequires:  qt-mysql >= 4.7.4
BuildRequires:  gnutls-devel
BuildRequires:  rrdtool-devel
BuildRequires:  make
BuildRequires:  centreon-clib
Requires:	qt-mysql >= 4.7.4
Requires:   qt-x11 >= 4.7.4
Requires:   rrdtool
Requires:   centreon-clib

%description
Centreon Broker %{version}

%prep
%setup -q


%build
cd build
# To disable modules, for example TLS, add:
#       -DWITH_MODULE_TLS=NO .
cmake28 \
    -DWITH_DAEMONS='central-broker;central-rrd' \
    -DWITH_GROUP=%{cent_broker_group} \
    -DWITH_PREFIX=%{cent_global_prefix} \
    -DWITH_PREFIX_CONF=%{cent_broker_etc} \
    -DWITH_STARTUP_DIR=/etc/init.d \
    -DWITH_STARTUP_SCRIPT=auto \
    -DWITH_TESTING=0 \
    -DWITH_USER=%{cent_broker_user} .
make -j3

%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/var/log/centreon-broker
mkdir -p %{buildroot}/var/lib/centreon-broker

%clean
rm -rf %{buildroot}

%pre
groupadd %{cent_broker_user} ||:
useradd -g %{cent_broker_group} -m -r -d /var/lib/centreon-broker %{cent_broker_user} ||:

%preun
service cbd stop
pkill -9 -u %{cent_broker_user}

%postun
userdel %{cent_broker_user}
groupdel %{cent_broker_group} ||:

%files
%attr(0755,%{cent_broker_user},%{cent_broker_group}) /var/log/centreon-broker
%attr(0750,%{cent_broker_user},%{cent_broker_group}) /var/lib/centreon-broker
%config(noreplace) %attr(0644,root,root) %{cent_broker_etc}/master.run
%attr(0755,root,root) /etc/init.d/cbd
%attr(0755,root,root) %{cent_global_prefix}/bin/cbd
%defattr(0644,root,root,-)
%{cent_global_prefix}/lib

%changelog
* Thu Aug 14 2014 Florent Peterschmitt <fpeterschmitt@capensis.fr>
- Init

%package cbmod

Summary:    Centreon Broker Module for Centreon Engine
Group:      Centreon
Requires:   centreon-engine

%description cbmod
Centreon Broker Module for Centreon Engine

%files cbmod
%defattr(0644,root,root,-)
%{cent_global_prefix}/lib/cbmod.so
