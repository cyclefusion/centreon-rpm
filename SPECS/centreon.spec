%define cent_global_prefix /usr/local/centreon-full/
%define cent_centreon_etc   /etc/centreon
%define cent_engine_user    centreon-engine
%define cent_engine_group   centreon-engine
%define cent_broker_user    centreon-broker
%define cent_broker_group   centreon-broker
%define cent_centreon_user  centreon
%define cent_centreon_group centreon
%define cent_apache_user    apache
%define cent_apache_group   apache

AutoReqProv: no

Name:		centreon
Version:	2.5.2
Release:	8%{?dist}
Summary:	Centreon Web

Group:		Centreon
License:	GPL
URL:		http://centreon.com
Source0:	%{name}-%{version}.tar.gz
Source1:    %{name}-%{version}.tmpl
Source2:    %{name}-%{version}-webinstall.sh
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch

BuildRequires:  centreon-engine
BuildRequires:  centreon-broker
Requires:   curl
Requires:   httpd
Requires:   centreon-engine
Requires:   centreon-broker-cbmod
Requires:   centreon-broker
Requires:	php
Requires:   php-mbstring
Requires:   php-mysql
Requires:   php-xml
Requires:   php-gd
Requires:   php-ldap
Requires:   php-pear-Auth-SASL
#Requires:   php-pear-Archive-Zip
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
#Requires:   php-pear-XML-RPC

%description
Centreon Web UI

%prep
rm -rf %{buildroot}/*
%setup -q
groupadd %{cent_centreon_user} ||:
useradd -g %{cent_centreon_user} -d /var/lib/centreon %{cent_centreon_user} ||:

%build
./install.sh -f %{SOURCE1} | grep FAIL > /tmp/%{name}-%{version}-install.log

%install
mkdir -p %{buildroot}/etc/cron.d/
mkdir -p %{buildroot}/var/run/centreon
mkdir -p %{buildroot}/var/lib/centreon/centplugins
mkdir -p %{buildroot}/var/lib/centreon/data
mkdir -p %{buildroot}/var/lib/centreon/rrd
mkdir -p %{buildroot}/var/lib/centreon/rrd/metrics
mkdir -p %{buildroot}/var/lib/centreon/rrd/status
mkdir -p %{buildroot}/var/log/centreon
mkdir -p %{buildroot}/usr/local/centreon-full/
mkdir -p %{buildroot}/var/spool/centreontrapd
mkdir -p %{buildroot}/etc/httpd/conf.d/
rm -rf %{buildroot}%{cent_global_prefix}/centreon/filesGeneration/*
cp -a %{cent_global_prefix}/centreon %{buildroot}%{cent_global_prefix}/

mkdir -p %{buildroot}/$(dirname %{cent_centreon_etc})
cp -a %{cent_centreon_etc} %{buildroot}/$(dirname %{cent_centreon_etc})

cp /etc/cron.d/centreon %{buildroot}/etc/cron.d/
cp /etc/httpd/conf.d/centreon.conf %{buildroot}/etc/httpd/conf.d/

mkdir -p %{buildroot}/usr/share/perl5/vendor_perl/
cp -r /usr/share/perl5/vendor_perl/centreon %{buildroot}/usr/share/perl5/vendor_perl/

mkdir -p %{buildroot}/etc/init.d
cp /etc/init.d/centcore /etc/init.d/centreontrapd %{buildroot}/etc/init.d/

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

%post
service mysqld restart
service httpd restart
. %{SOURCE2}
mv %{cent_global_prefix}/centreon/www/install %{cent_global_prefix}/centreon/www/install-$(date +%s)
chkconfig centcore on
chkconfig centreontrapd on
chkconfig snmptrapd on
service centcore start
service centreontrapd start
service snmptrapd start

%preun
service centcore stop
service centreontrapd stop
service snmptrapd stop

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
rm -rf %{cent_centreon_etc}
rm -rf /var/log/centreon
rm -rf /var/lib/centreon
rm -rf /var/run/centreon
rm -rf /etc/cron.d/centreon
rm -rf /var/spool/centreontrapd
rm -rf /var/lib/centreon/centplugins
rm -rf /usr/share/perl5/vendor_perl/centreon
rm -rf /etc/init.d/centcore
rm -rf /etc/init.d/centreontrapd
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
%defattr(0755,root,root,-)
/etc/init.d/centcore
/etc/init.d/centreontrapd

%defattr(0755,root,root,0755)
%{cent_global_prefix}/centreon/bin
%defattr(0644,root,root,0755)
%{cent_global_prefix}/centreon/examples
%{cent_global_prefix}/centreon/libinstall

%config(noreplace) /etc/cron.d/centreon
%config(noreplace) /etc/httpd/conf.d/centreon.conf

# setup configuration files
%attr(0775,root,%{cent_centreon_group}) %dir %{cent_centreon_etc}
%attr(0640,root,%{cent_centreon_group}) %config(noreplace) %{cent_centreon_etc}/*

# setup generation directories
%attr(0755,root,root) %dir %{cent_global_prefix}/centreon/filesGeneration
%attr(2770,%{cent_centreon_user},%{cent_centreon_group}) %dir %{cent_global_prefix}/centreon/filesGeneration/broker
%attr(2770,%{cent_centreon_user},%{cent_centreon_group}) %dir %{cent_global_prefix}/centreon/filesGeneration/nagiosCFG

# setup storages
%attr(0775,%{cent_centreon_user},%{cent_centreon_group}) %dir /var/lib/centreon
%attr(0755,root,root) %dir /var/lib/centreon/data
%attr(0775,%{cent_centreon_user},%{cent_centreon_group}) %dir /var/lib/centreon/centplugins
%attr(0775,%{cent_centreon_user},%{cent_centreon_group}) %dir /var/lib/centreon/rrd
%attr(0775,%{cent_centreon_user},%{cent_centreon_group}) %dir /var/log/centreon

# setup www
%defattr(0644,%{cent_centreon_user},%{cent_centreon_group},0755)
%{cent_global_prefix}/centreon/GPL_LIB
%{cent_global_prefix}/centreon/cron
%{cent_global_prefix}/centreon/www

%defattr(2664,%{cent_centreon_user},%{cent_centreon_group},2775)
%{cent_global_prefix}/centreon/GPL_LIB/SmartyCache/compile
%{cent_global_prefix}/centreon/www/install

%defattr(644,root,root,755)
/usr/share/perl5/vendor_perl/centreon

%changelog
* Thu Aug 14 2014 Florent Peterschmitt <fpeterschmitt@capensis.fr>
- Init
