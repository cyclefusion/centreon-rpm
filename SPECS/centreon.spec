%define cent_global_prefix /usr/local/centreon-full/
%define cent_engine_user    centreon-engine
%define cent_engine_group   centreon-engine
%define cent_broker_user    centreon-broker
%define cent_broker_group   centreon-broker
%define cent_centreon_user  centreon
%define cent_centreon_group centreon
%define cent_apache_user    apache
%define cent_apache_group   apache

Name:		centreon
Version:	2.5.2
Release:	1%{?dist}
Summary:	Centreon Web

Group:		Centreon
License:	GPL
URL:		http://centreon.com
Source0:	%{name}-%{version}.tar.gz
Source1:    %{name}-%{version}.tmpl
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch

BuildRequires:  centreon-engine
BuildRequires:  centreon-broker
Requires:   centreon-engine
Requires:   centreon-engine-cbmod
Requires:   centreon-broker
Requires:	php
Requires:   php-mbstring
Requires:   php-mysql
Requires:   php-xml
Requires:   php-gd
Requires:   php-ldap
Requires:   php-pear-Auth-SASL
Requires:   php-pear-Archive-Zip
Requires:   php-pear-Date
Requires:   php-pear-DB-DataObject
Requires:   php-pear-DB-DataObject-FormBuilder
Requires:   php-pear-HTML-Common
Requires:   php-pear-HTML-QuickForm
Requires:   php-pear-HTML-QuickForm-advmultiselect
Requires:   php-pear-HTML-Table
Requires:   php-pear-Log
Requires:   php-pear-Net-SMTP
Requires:   php-pear-Net-Socket
Requires:   php-pear-Net-Traceroute
Requires:   php-pear-Net-Ping
Requires:   php-pear-SOAP
Requires:   php-pear-Validate
Requires:   php-pear-XML-RPC
Requires:   httpd

%description
Centreon Web UI

%prep
rm -rf %{buildroot}/*
%setup -q
groupadd %{cent_centreon_user} ||:
useradd -g %{cent_centreon_user} -d /var/lib/centreon %{cent_centreon_user} ||:

%build
./install.sh -f %{SOURCE1}

%install
mkdir -p %{buildroot}/etc/cron.d/
mkdir -p %{buildroot}/var/run/centreon
mkdir -p %{buildroot}/var/lib/centreon/data
mkdir -p %{buildroot}/var/lib/centreon/rrd
mkdir -p %{buildroot}/var/log/centreon
mkdir -p %{buildroot}/usr/local/centreon-full/
mkdir -p %{buildroot}/var/spool/centreontrapd
mkdir -p %{buildroot}/etc/httpd/conf.d/
rm -rf %{buildroot}%{cent_global_prefix}/centreon/filesGeneration/*
mv %{cent_global_prefix}/centreon %{buildroot}%{cent_global_prefix}/
cp /etc/cron.d/centreon %{buildroot}/etc/cron.d/
cp /etc/httpd/conf.d/centreon.conf %{buildroot}/etc/httpd/conf.d/

%pre
groupadd %{cent_centreon_user}
useradd -g %{cent_centreon_user} -d /var/lib/centreon %{cent_centreon_user}
usermod -a -G %{cent_centreon_group} %{cent_apache_user}
usermod -a -G %{cent_centreon_group} %{cent_engine_user}
usermod -a -G %{cent_engine_group} %{cent_apache_user}
usermod -a -G %{cent_engine_group} %{cent_centreon_user}
usermod -a -G %{cent_broker_group} %{cent_apache_user}
usermod -a -G %{cent_broker_group} %{cent_engine_user}
usermod -a -G %{cent_centreon_group} %{cent_broker_user}
service httpd restart

%postun
gpasswd -d %{cent_apache_user} %{cent_centreon_group}
gpasswd -d %{cent_engine_user} %{cent_centreon_group}
gpasswd -d %{cent_apache_user} %{cent_engine_group}
gpasswd -d %{cent_centreon_user} %{cent_engine_group}
gpasswd -d %{cent_apache_user} %{cent_broker_group}
gpasswd -d %{cent_engine_user} %{cent_broker_group}
gpasswd -d %{cent_broker_user} %{cent_centreon_group}
pkill -u -9 %{cent_centreon_user} ||:
userdel %{cent_centreon_user}
groupdel %{cent_centreon_group} ||:

%clean
rm -rf %{buildroot}
rm -rf /etc/httpd/conf.d/centreon.conf
rm -rf %{cent_global_prefix}/centreon
rm -rf /etc/centreon
rm -rf /var/log/centreon
rm -rf /var/lib/centreon
rm -rf /var/run/centreon
rm -rf /etc/cron.d/centreon
rm -rf /var/spool/centreontrapd
gpasswd -d %{cent_apache_user} %{cent_centreon_group}
gpasswd -d %{cent_engine_user} %{cent_centreon_group}
gpasswd -d %{cent_apache_user} %{cent_engine_group}
gpasswd -d %{cent_centreon_user} %{cent_engine_group}
gpasswd -d %{cent_apache_user} %{cent_broker_group}
gpasswd -d %{cent_engine_user} %{cent_broker_group}
gpasswd -d %{cent_broker_user} %{cent_centreon_group}
pkill -u -9 %{cent_centreon_user} ||:
userdel %{cent_centreon_user}
groupdel %{cent_centreon_group} ||:

%files
%dir %{cent_global_prefix}/centreon/filesGeneration
%dir /var/lib/centreon
%dir /var/lib/centreon/rrd
%dir /var/log/centreon
%{cent_global_prefix}/centreon/GPL_LIB
%{cent_global_prefix}/centreon/bin
%{cent_global_prefix}/centreon/cron
%{cent_global_prefix}/centreon/examples
%{cent_global_prefix}/centreon/libinstall
%{cent_global_prefix}/centreon/www
/etc/cron.d/centreon
/etc/httpd/conf.d/centreon.conf

%changelog
* Thu Aug 14 2014 Florent Peterschmitt <fpeterschmitt@capensis.fr>
- Init
