%define cent_centreon_user  centreon
%define cent_centreon_group centreon

Name:		centreon-poller-ssh
Version:	1
Release:	1%{?dist}
Summary:	Centreon private SSH keys

Group:		Centreon
License:	None
URL:		none
Source0:	%{name}-rsa-private
Source1:	%{name}-rsa-public
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Centreon private SSH keys, used by CentCore.


%prep
mkdir -p %{buildroot}

%build

%install
install -d -m0700 -o %{cent_centreon_user} -g %{cent_centreon_group} %{%{buildroot}/var/lib/centreon-engine/.ssh
cp %{SOURCE0} %{buildroot}/var/lib/centreon-engine/.ssh/authorized_keys

%post
cat /var/lib/centreon-engine/.ssh/id_rsa-%{name}.pub >> /var/lib/centreon-engine/.ssh

%clean
rm -rf %{buildroot}

%files
%defattr(-,%{cent_centreon_user},%{cent_centreon_group},-)
/var/lib/centreon-engine/.ssh

%changelog

