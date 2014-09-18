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

Name:       centreon
Version:    2.5.2
Release:    21%{?dist}
Summary:    Centreon Web

Group:      Centreon
License:    GPL
URL:        http://centreon.com
Source0:    %{name}-%{version}.tar.gz
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch

BuildRequires:	mailx
BuildRequires:	postfix
BuildRequires:  cronie
BuildRequires:  sudo
BuildRequires:  net-snmp
BuildRequires:  centreon-configuration-install
BuildRequires:  centreon-engine
BuildRequires:  centreon-broker
BuildRequires:  php
BuildRequires:  php-mbstring
BuildRequires:  php-mysql
BuildRequires:  php-xml
BuildRequires:  php-gd
BuildRequires:  php-ldap
BuildRequires:  php-pear-Auth-SASL
BuildRequires:  php-pear-Date
BuildRequires:  php-pear-DB-DataObject
BuildRequires:  php-pear-DB-DataObject-FormBuilder
BuildRequires:  php-pear-HTML-Common
BuildRequires:  php-pear-HTML-QuickForm
BuildRequires:  php-pear-HTML-QuickForm-advmultiselect
BuildRequires:  php-pear-HTML-Table
BuildRequires:  php-pear-Log
BuildRequires:  php-pear-Net-SMTP
BuildRequires:  php-pear-Net-Socket
BuildRequires:  php-pear-Net-Traceroute
BuildRequires:  php-pear-Net-Ping
BuildRequires:  php-pear-SOAP
BuildRequires:  php-pear-Validate
# Custom php-pear packages
BuildRequires:  php-pear-Archive-Zip

AutoReqProv: no

Requires:   redhat-lsb-core
Requires:   mailx
Requires:   postfix
Requires:   cronie
Requires:   net-snmp
Requires:   sudo
Requires:   curl
Requires:   httpd
Requires:   centreon-engine
Requires:   centreon-broker-cbmod
Requires:   centreon-broker
Requires:   perl-DBD-MySQL
Requires:   php
Requires:   php-mbstring
Requires:   php-mysql
Requires:   php-xml
Requires:   php-gd
Requires:   php-ldap
Requires:   php-pear-Auth-SASL
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
# Custom php-pear packages
Requires:   php-pear-Archive-Zip
Requires:   centreon-configuration-install

%define install_dir /usr/share/centreon-webui-%{version}

%description
Centreon Web UI

%prep
rm -rf %{buildroot}/*

%setup -q

groupadd %{cent_centreon_user} ||:
useradd -g %{cent_centreon_user} -d /var/lib/centreon %{cent_centreon_user} ||:

%build
./install.sh -f %{install_dir}/template # | grep FAIL > /tmp/%{name}-%{version}-install.log

%install
mkdir -p %{buildroot}/etc/cron.d/
mkdir -p %{buildroot}/etc/httpd/conf.d/
mkdir -p %{buildroot}/etc/init.d
mkdir -p %{buildroot}/etc/sudoers.d
mkdir -p %{buildroot}/var/lib/centreon/centplugins
mkdir -p %{buildroot}/var/lib/centreon/data
mkdir -p %{buildroot}/var/lib/centreon/rrd/metrics
mkdir -p %{buildroot}/var/lib/centreon/rrd/status
mkdir -p %{buildroot}/var/log/centreon
mkdir -p %{buildroot}/var/run/centreon
mkdir -p %{buildroot}/var/spool/centreontrapd
mkdir -p %{buildroot}%{cent_global_prefix}/libexec

sudo_start=$(grep -n "BEGIN: CENTREON SUDO" /etc/sudoers|cut -f1 -d:)
sudo_end=$(grep -n "END: CENTREON SUDO" /etc/sudoers|cut -f1 -d:)
 
sed -n ${sudo_start},${sudo_end}p /etc/sudoers > %{buildroot}/etc/sudoers.d/centreon
sed ${sudo_start},${sudo_end}d -i /etc/sudoers

rm -rf %{cent_global_prefix}/centreon/filesGeneration/broker/*
rm -rf %{cent_global_prefix}/centreon/filesGeneration/nagiosCFG/*
rm -rf %{cent_global_prefix}/centreon/www/install-[0-9]*
cp -a %{cent_global_prefix}/centreon %{buildroot}%{cent_global_prefix}/

mkdir -p %{buildroot}/$(dirname %{cent_centreon_etc})
cp -a %{cent_centreon_etc} %{buildroot}/$(dirname %{cent_centreon_etc})

cp /etc/cron.d/centreon %{buildroot}/etc/cron.d/
cp /etc/cron.d/centstorage %{buildroot}/etc/cron.d/
cp /etc/httpd/conf.d/centreon.conf %{buildroot}/etc/httpd/conf.d/

mkdir -p %{buildroot}/usr/share/perl5/vendor_perl/
cp -r /usr/share/perl5/vendor_perl/centreon %{buildroot}/usr/share/perl5/vendor_perl/

# We install CentCore and CentreonTrapd services, NOT CentStorage.
cp /etc/init.d/centcore /etc/init.d/centreontrapd %{buildroot}/etc/init.d/

cp -r %{cent_global_prefix}/libexec/Centreon %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/centreon.conf %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/centreon.pm %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_dummy %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_MS_multiple_services %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_ping %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_cpu %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_loadaverage %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_memory %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_multiple_process %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_packetErrors %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_process %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_process_detailed %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_remote_storage %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_string %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_TcpConn %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_traffic %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_uptime %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_value %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_centreon_snmp_value_table.pl %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_meta_service %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_snmp_cpfw.pl %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_snmp_load.pl %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_snmp_mem.pl %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_snmp_process.pl %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_snmp_script_result.pl %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_snmp_storage.pl %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/check_snmp_win.pl %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/process-service-perfdata %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/submit_host_check_result %{buildroot}%{cent_global_prefix}/libexec/
cp -r %{cent_global_prefix}/libexec/submit_service_check_result %{buildroot}%{cent_global_prefix}/libexec/

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
service httpd restart
if [ ! "$1" = "2" ]&&[ ! -f %{cent_global_prefix}/centreon_webui_no_websetup ]; then
    echo "Running websetup for initial setup. Few minutes needed." 1>&2
    . %{install_dir}/webinstall.sh %{install_dir} && mv %{cent_global_prefix}/centreon/www/install %{cent_global_prefix}/centreon/www/install-$(date +%s)
elif [ -f %{cent_global_prefix}/centreon_webui_no_websetup ]; then
    echo "%{cent_global_prefix}/centreon_webui_no_websetup exists: no automatic websetup ran. You can run it yourself if you want:" 1>&2
    echo ". %{install_dir}/webinstall.sh && mv %{cent_global_prefix}/centreon/www/install %{cent_global_prefix}/centreon/www/install-$(date +%s)" 1>&2
else
cat 1>&2 << EOF
WARNING:
   Websetup not made because of upgrade.
   o If it is a primary installation, you can run websetup that way:
. %{install_dir}/webinstall.sh && mv %{cent_global_prefix}/centreon/www/install %{cent_global_prefix}/centreon/www/install-$(date +%s)
   o If it is an upgrade, go to the web interface and follow upgrade process.
WEB UPGRADE:
   o Depending of your current installation, SQL scripts can fail to upgrade.
   o It *should* be safe to just comment lines that fails and refresh the upgrade to continue.
   o However, always do a backup of centreon, centreon_storage and centreon_status *before* doing the upgrade.
   o If you messed up your installation, you can safely restore your database backups, remove the package and re-install it.
     You will get some errors about existing database when websetup but it is okay.
   o Once you upgraded all databases and went to the finish message, remove %{cent_global_prefix}/centreon/www/install or you willll loop in upgrade page.
About the package:
   o This package will *NEVER* delete any database.
   o This package will *NEVER* do database upgrades automaticaly.
   o This package *CAN* be safely removed and re-installed.
   o If you dont want automatic websetup to be run, create this file: %{cent_global_prefix}/centreon_webui_no_websetup
EOF

fi

chkconfig httpd on
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
pkill -9 -u %{cent_centreon_user} ||:

%postun
if [ ! "$1" = "2" ]; then
    chkconfig centcore off
    chkconfig centreontrapd off
    #rm -rf %{cent_centreon_etc}
    gpasswd -d %{cent_apache_user} %{cent_centreon_group}
    gpasswd -d %{cent_engine_user} %{cent_centreon_group}
    gpasswd -d %{cent_apache_user} %{cent_engine_group}
    gpasswd -d %{cent_centreon_user} %{cent_engine_group}
    gpasswd -d %{cent_apache_user} %{cent_broker_group}
    gpasswd -d %{cent_engine_user} %{cent_broker_group}
    gpasswd -d %{cent_broker_user} %{cent_centreon_group}
    userdel %{cent_centreon_user}
    groupdel %{cent_centreon_group} ||:
    echo "You can drop databases by running this command:"
    echo ". %{install_dir}/webinstall.sh %{install_dir}"
fi

%clean
rm -rf %{buildroot}
rm -rf /etc/httpd/conf.d/centreon.conf
rm -rf %{cent_global_prefix}/centreon
rm -rf %{cent_centreon_etc}
rm -rf /var/log/centreon
rm -rf /var/lib/centreon
rm -rf /var/run/centreon
rm -rf /etc/cron.d/centreon
rm -rf /etc/cron.d/centstorage
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
pkill -9 -u %{cent_centreon_user} ||:
userdel %{cent_centreon_user}
groupdel %{cent_centreon_group} ||:

rm -rf %{cent_global_prefix}/libexec/Centreon
rm -rf %{cent_global_prefix}/libexec/centreon.conf
rm -rf %{cent_global_prefix}/libexec/centreon.pm
rm -rf %{cent_global_prefix}/libexec/check_centreon_dummy
rm -rf %{cent_global_prefix}/libexec/check_centreon_MS_multiple_services
rm -rf %{cent_global_prefix}/libexec/check_centreon_ping
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_cpu
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_loadaverage
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_memory
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_multiple_process
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_packetErrors
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_process
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_process_detailed
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_remote_storage
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_string
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_TcpConn
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_traffic
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_uptime
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_value
rm -rf %{cent_global_prefix}/libexec/check_centreon_snmp_value_table.pl
rm -rf %{cent_global_prefix}/libexec/check_meta_service
rm -rf %{cent_global_prefix}/libexec/check_snmp_cpfw.pl
rm -rf %{cent_global_prefix}/libexec/check_snmp_load.pl
rm -rf %{cent_global_prefix}/libexec/check_snmp_mem.pl
rm -rf %{cent_global_prefix}/libexec/check_snmp_process.pl
rm -rf %{cent_global_prefix}/libexec/check_snmp_script_result.pl
rm -rf %{cent_global_prefix}/libexec/check_snmp_storage.pl
rm -rf %{cent_global_prefix}/libexec/check_snmp_win.pl
rm -rf %{cent_global_prefix}/libexec/process-service-perfdata
rm -rf %{cent_global_prefix}/libexec/submit_host_check_result
rm -rf %{cent_global_prefix}/libexec/submit_service_check_result

%files
%defattr(0755,root,root,-)
/etc/init.d/centcore
/etc/init.d/centreontrapd

%defattr(0755,root,root,0755)
%{cent_global_prefix}/centreon/bin
%defattr(0644,root,root,0755)
%{cent_global_prefix}/centreon/examples
%{cent_global_prefix}/centreon/libinstall

# Cron, apache, sudo
%config(noreplace) /etc/cron.d/centreon
%config(noreplace) /etc/cron.d/centstorage
%config(noreplace) /etc/httpd/conf.d/centreon.conf
%attr(0640,root,root) /etc/sudoers.d/centreon

# setup configuration files
%attr(0775,root,%{cent_centreon_group}) %config %dir %{cent_centreon_etc}
%attr(0640,root,%{cent_centreon_group}) %config(noreplace) %{cent_centreon_etc}/*

# setup generation directories
%attr(0755,root,root) %dir %{cent_global_prefix}/centreon/filesGeneration
%attr(2770,%{cent_centreon_user},%{cent_centreon_group}) %dir %{cent_global_prefix}/centreon/filesGeneration/broker
%attr(2770,%{cent_centreon_user},%{cent_centreon_group}) %dir %{cent_global_prefix}/centreon/filesGeneration/nagiosCFG

# setup storages
%attr(0775,%{cent_centreon_user},%{cent_centreon_group}) %dir /var/lib/centreon
%attr(0755,root,root) %dir /var/lib/centreon/data
%defattr(0660,%{cent_centreon_user},%{cent_centreon_group},0770)
/var/lib/centreon/centplugins
/var/lib/centreon/rrd
/var/lib/centreon/rrd/metrics
/var/lib/centreon/rrd/status
/var/log/centreon

# setup www
%defattr(0644,root,root,0755)
%{cent_global_prefix}/centreon/GPL_LIB/
%{cent_global_prefix}/centreon/cron/
%attr(0755,root,root) %dir %{cent_global_prefix}/centreon/www
%{cent_global_prefix}/centreon/www/class
%{cent_global_prefix}/centreon/www/img
%{cent_global_prefix}/centreon/www/include
%{cent_global_prefix}/centreon/www/lib
%{cent_global_prefix}/centreon/www/menu
%{cent_global_prefix}/centreon/www/sounds
%{cent_global_prefix}/centreon/www/Themes
%{cent_global_prefix}/centreon/www/widgets
%{cent_global_prefix}/centreon/www/*.php
%{cent_global_prefix}/centreon/www/*.txt

%defattr(6664,%{cent_centreon_user},%{cent_centreon_group},6775)
%{cent_global_prefix}/centreon/GPL_LIB/SmartyCache/compile

%defattr(0770,%{cent_apache_user},%{cent_apache_group},6770)
%{cent_global_prefix}/centreon/www/install/

%defattr(644,root,root,755)
/usr/share/perl5/vendor_perl/centreon

%package plugins
Summary:    Centreon Plugins
Group:      Centreon

AutoReqProv: no
Requires:   perl(utils)
Requires:   perl(Config::IniFiles)
Requires:   perl(IO::Scalar)
Requires:   perl(List::MoreUtils)

%description plugins
Centreon Plugins

%files plugins
%defattr(0755,root,root,0755)
%{cent_global_prefix}/libexec/Centreon
%{cent_global_prefix}/libexec/centreon.conf
%{cent_global_prefix}/libexec/centreon.pm
%{cent_global_prefix}/libexec/check_centreon_dummy
%{cent_global_prefix}/libexec/check_centreon_MS_multiple_services
%attr(1755,root,root) %{cent_global_prefix}/libexec/check_centreon_ping
%{cent_global_prefix}/libexec/check_centreon_snmp_cpu
%{cent_global_prefix}/libexec/check_centreon_snmp_loadaverage
%{cent_global_prefix}/libexec/check_centreon_snmp_memory
%{cent_global_prefix}/libexec/check_centreon_snmp_multiple_process
%{cent_global_prefix}/libexec/check_centreon_snmp_packetErrors
%{cent_global_prefix}/libexec/check_centreon_snmp_process
%{cent_global_prefix}/libexec/check_centreon_snmp_process_detailed
%{cent_global_prefix}/libexec/check_centreon_snmp_remote_storage
%{cent_global_prefix}/libexec/check_centreon_snmp_string
%{cent_global_prefix}/libexec/check_centreon_snmp_TcpConn
%{cent_global_prefix}/libexec/check_centreon_snmp_traffic
%{cent_global_prefix}/libexec/check_centreon_snmp_uptime
%{cent_global_prefix}/libexec/check_centreon_snmp_value
%{cent_global_prefix}/libexec/check_centreon_snmp_value_table.pl
%{cent_global_prefix}/libexec/check_meta_service
%{cent_global_prefix}/libexec/check_snmp_cpfw.pl
%{cent_global_prefix}/libexec/check_snmp_load.pl
%{cent_global_prefix}/libexec/check_snmp_mem.pl
%{cent_global_prefix}/libexec/check_snmp_process.pl
%{cent_global_prefix}/libexec/check_snmp_script_result.pl
%{cent_global_prefix}/libexec/check_snmp_storage.pl
%{cent_global_prefix}/libexec/check_snmp_win.pl
%{cent_global_prefix}/libexec/process-service-perfdata
%{cent_global_prefix}/libexec/submit_host_check_result
%{cent_global_prefix}/libexec/submit_service_check_result

%changelog
* Thu Aug 14 2014 Florent Peterschmitt <fpeterschmitt@capensis.fr>
- Init
