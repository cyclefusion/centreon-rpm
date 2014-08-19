%define centreon_version 2.5.2
%define install_dir /usr/share/centreon-webui-%{centreon_version}/
%define type_install local

Name:		centreon-configuration-install-%{type_install}
Version:	%{centreon_version}
Release:	4%{?dist}
Summary:	Template and websetup scripts

Group:		Centreon
License:	GPL
Source0:	centreon-%{centreon_version}.tmpl
Source1:    centreon-%{centreon_version}-webinstall-%{type_install}.sh
Source2:    centreon-%{centreon_version}-deinstall-%{type_install}.sh
Source3:    centreon-%{centreon_version}-configuration-%{type_install}.sh
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	curl


Provides:   centreon-configuration-install
Obsoletes:  centreon-configuration-install

%description
Installation template and websetup script for Centreon Web UI.

%prep

%build

%install
mkdir -p %{buildroot}/usr/share/centreon-webui-%{centreon_version}/
cp %{SOURCE0} %{buildroot}%{install_dir}/template
cp %{SOURCE1} %{buildroot}%{install_dir}/webinstall.sh
cp %{SOURCE2} %{buildroot}%{install_dir}/deinstall.sh
cp %{SOURCE3} %{buildroot}%{install_dir}/configuration.sh

%clean

%files
%defattr(0750,root,root,0750)
%{install_dir}

%changelog

