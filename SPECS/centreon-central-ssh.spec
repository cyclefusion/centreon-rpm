%define cent_centreon_user  centreon
%define cent_centreon_group centreon
%define cent_configuration  local

Name:		centreon-central-ssh-%{cent_configuration}
Version:	1
Release:	1%{?dist}
Summary:	Centreon private SSH keys
Group:		Centreon
License:    none
Source0:	%{name}-rsa-private
Source1:	%{name}-rsa-public
Source3:    %{name}-ssh-config
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch

#Make another spec/rpm for each configuration, with a meaningful name.
#At central install, dont forget to install your custom package and to make
#another package providing centreon-poller-ssh, with the correct
#pubkey configured.

Obsoletes: centreon-central-ssh
Provides:  centreon-central-ssh

%description
Centreon private SSH keys, used by CentCore.

%prep
mkdir -p %{buildroot}

%build

%install
mkdir -p %{buildroot}/var/lib/centreon/.ssh
cp %{SOURCE0} %{buildroot}/var/lib/centreon/.ssh/id_rsa
cp %{SOURCE1} %{buildroot}/var/lib/centreon/.ssh/id_rsa.pub
# ssh config can be used to define custom logins
cp %{SOURCE3} %{buildroot}/var/lib/centreon/.ssh/config

%clean
rm -rf %{buildroot}

%files
%defattr(0600,%{cent_centreon_user},%{cent_centreon_group},0700)
/var/lib/centreon/.ssh

%changelog
* Tue Aug 19 2014 Florent Peterschmitt <fpeterschmitt@capensis.fr>
- Init
