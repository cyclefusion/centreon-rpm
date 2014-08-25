Name:       centreon-configuration-poller-sudo
Version:    2.5.2
Release:    1%{?dist}
Summary:    Sudo configration for poller

Group:      Centreon
License:    none
URL:        https://git.beastie.eu/capensis/centreon-rpm
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch

Requires:   sudo

%description
Sudo configuration for poller


%prep
rm -rf %{buildroot}/*

%build

%install
mkdir -p %{buildroot}/etc/sudoers.d
%{__cat} >> %{buildroot}/etc/sudoers.d/centreon << EOF
## BEGIN: CENTREON SUDO
#Add by CENTREON installation script
User_Alias      CENTREON=centreon-engine
Defaults:CENTREON !requiretty
# Monitoring engine Restart
CENTREON   ALL = NOPASSWD: /etc/init.d/centengine* restart
CENTREON   ALL = NOPASSWD: /etc/init.d/centengine restart
# Monitoring engine reload
CENTREON   ALL = NOPASSWD: /etc/init.d/centengine* reload
CENTREON   ALL = NOPASSWD: /etc/init.d/centengine reload
# Monitoring engine force-reload
CENTREON   ALL = NOPASSWD: /etc/init.d/centengine* force-reload
CENTREON   ALL = NOPASSWD: /etc/init.d/centengine force-reload
# Monitoring engine test config
CENTREON   ALL = NOPASSWD: /usr/local/centreon-full/bin/centengine* -v *
CENTREON   ALL = NOPASSWD: /usr/local/centreon-full/bin/centengine -v *
# Monitoring engine test for optim config
CENTREON   ALL = NOPASSWD: /usr/local/centreon-full/bin/centengine* -s *
CENTREON   ALL = NOPASSWD: /usr/local/centreon-full/bin/centengine -s *
EOF

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config /etc/sudoers.d/centreon


%changelog

