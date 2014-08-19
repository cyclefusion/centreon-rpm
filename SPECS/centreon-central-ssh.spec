%define cent_centreon_user  centreon
%define cent_centreon_group centreon

Name:		centreon-central-ssh
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

%build

%install
install -d -m0700 -o %{cent_centreon_user} -g %{cent_centreon_group} %{%{buildroot}/var/lib/centreon/.ssh
cp %{SOURCE0} %{buildroot}/var/lib/centreon/.ssh/id_rsa
cp %{SOURCE1} %{buildroot}/var/lib/centreon/.ssh/id_rsa.pub

%clean
rm -rf %{buildroot}


%files
%defattr(-,%{cent_centreon_user},%{cent_centreon_group},-)
/var/lib/centreon/.ssh

%changelog

