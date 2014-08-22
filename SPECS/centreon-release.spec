Name:		centreon-release
Version:	1
Release:	1%{?dist}
Summary:	CentOS6 Centreon release package

Group:		Centreon
License:	none
URL:		https://git.beastie.eu/capensis/centreon-rpm
Source0:	%{name}.repo
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

%description
CentOS6 Centreon release package


%prep
mkdir -p %{buildroot}

%build

%install
mkdir -p %{buildroot}/etc/yum.repos.d/
cp %{SOURCE0} %{buildroot}/etc/yum.repos.d/centreon-repos.beastie.eu.repo

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/etc/yum.repos.d/centreon-repos.beastie.eu.repo


%changelog

