Name:		meta-centreon-poller
Version:	1
Release:	2%{?dist}
Summary:    Install a poller with Centreon Engine, Centreon Broker Module and Nagios Plugins

Group:		Centreon
License:	GPL
URL:		http://centreon.com
BuildArch:  noarch

Requires:   sudo
Requires:   centreon-plugins-nagios
Requires:	centreon-engine
Requires:   centreon-broker-cbmod
Requires:   centreon-configuration-poller-ssh

%description
Install a poller with Centreon Engine, Centreon Broker Module and Nagios Plugins

%prep

%build

%install

%clean

%files

%changelog
* Thu Aug 14 2014 Florent Peterschmitt <fpeterschmitt@capensis.fr>
- Init
