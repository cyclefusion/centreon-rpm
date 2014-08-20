Name:		meta-centreon-central
Version:	1
Release:	1%{?dist}
Summary:	Install a complete Centreon Web UI, Engine and Broker platform

Group:		Centreon
License:	GPL
URL:		http://centreon.com
BuildArch:  noarch

Requires:   centreon-plugins-nagios
Requires:	centreon-engine
Requires:   centreon-broker-cbmod
Requires:   centreon-broker
Requires:   centreon-configuration-central-ssh
Requires:   centreon

%description
Install a complete Centreon Web UI, Engine and Broker platform

%prep

%build

%install

%clean

%files

%changelog
* Thu Aug 14 2014 Florent Peterschmitt <fpeterschmitt@capensis.fr>
- Init
