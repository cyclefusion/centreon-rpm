%define cent_global_prefix /usr/local/centreon-full/
%define _pname nagios-plugins

Name:		centreon-plugins-nagios
Version:	2.0.3
Release:	1%{?dist}
Summary:	Nagios plugins for Centreon

Group:		Centreon
License:	GPL
URL:		http://nagios-plugins.org/
Source0:	%{_pname}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	mysql-devel
BuildRequires:  postgresql-devel
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
Requires:	perl

%description
Nagios plugins for Centreon

%prep
%setup -q -n %{_pname}-%{version}


%build
./configure --prefix=%{cent_global_prefix} --enable-perl-modules
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{cent_global_prefix}/libexec/
%{cent_global_prefix}/perl/bin/
%{cent_global_prefix}/perl/lib/
%{cent_global_prefix}/perl/man/
%{cent_global_prefix}/share/

%changelog
* Thu Aug 14 2014 Florent Peterschmitt <fpeterschmitt@capensis.fr>
- Init
