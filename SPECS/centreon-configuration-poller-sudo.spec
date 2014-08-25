Name:       centreon-configuration-poller-sudo
Version:    2.5.2
Release:    3%{?dist}
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
%{__cat} >> %{buildroot}/etc/sudoers.d/centreon-poller << EOF
## BEGIN: CENTREONPOLLER SUDO
User_Alias      CENTREONPOLLER=centreon-engine
Defaults:CENTREONPOLLER !requiretty
CENTREONPOLLER   ALL = NOPASSWD: /etc/init.d/centengine* restart
CENTREONPOLLER   ALL = NOPASSWD: /etc/init.d/centengine restart
CENTREONPOLLER   ALL = NOPASSWD: /etc/init.d/centengine* reload
CENTREONPOLLER   ALL = NOPASSWD: /etc/init.d/centengine reload
CENTREONPOLLER   ALL = NOPASSWD: /etc/init.d/centengine* force-reload
CENTREONPOLLER   ALL = NOPASSWD: /etc/init.d/centengine force-reload
CENTREONPOLLER   ALL = NOPASSWD: /usr/local/centreon-full/bin/centengine* -v *
CENTREONPOLLER   ALL = NOPASSWD: /usr/local/centreon-full/bin/centengine -v *
CENTREONPOLLER   ALL = NOPASSWD: /usr/local/centreon-full/bin/centengine* -s *
CENTREONPOLLER   ALL = NOPASSWD: /usr/local/centreon-full/bin/centengine -s *
EOF

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config /etc/sudoers.d/centreon-poller


%changelog

