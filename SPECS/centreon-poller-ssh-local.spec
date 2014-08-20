%define cent_centreon_user  centreon
%define cent_centreon_group centreon
%define cent_configuration  local

Name:		centreon-poller-ssh-%{cent_configuration}
Version:	1
Release:	1%{?dist}
Summary:	Centreon private SSH keys

Group:		Centreon
License:	None
URL:		none
Source0:	%{name}-authorized_keys
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch

#Make another spec/rpm for each configuration, with a meaningful name.
#At poller install, dont forget to provide your custom package on command line.
Obsoletes: centreon-poller-ssh
Provides:  centreon-poller-ssh

%description
Centreon private SSH keys, used by CentCore.


%prep
mkdir -p %{buildroot}

%build

%install
mkdir -p %{buildroot}/var/lib/centreon-engine/.ssh
cat %{SOURCE0} > %{buildroot}/var/lib/centreon-engine/.ssh/authorized_keys

%post

%clean
rm -rf %{buildroot}

%files
%defattr(0600,%{cent_centreon_user},%{cent_centreon_group},0700)
/var/lib/centreon-engine/.ssh

%changelog

