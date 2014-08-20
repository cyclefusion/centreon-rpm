%define peardir %(pear config-get php_dir 2> /dev/null || echo %{_datadir}/pear)
%define xmldir  /var/lib/pear

Summary:    PHP implementation of the XML-RPC protocol
Name:       php-pear-XML-RPC
Version:    1.5.5
Release:    1
License:    PHP License
Group:      Development/Libraries
Source0:    http://pear.php.net/get/XML_RPC-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
URL:        http://pear.php.net/package/XML_RPC
BuildRequires:  php-pear
Requires:       php-pear

BuildArch: noarch

%description
A PEAR-ified version of Useful Inc's XML-RPC for PHP.

It has support for HTTP/HTTPS transport, proxies and authentication.

%prep
%setup -c -T
pear -v -c pearrc \
        -d php_dir=%{peardir} \
        -d doc_dir=/docs \
        -d bin_dir=%{_bindir} \
        -d data_dir=%{peardir}/data \
        -d test_dir=%{peardir}/tests \
        -d ext_dir=%{_libdir} \
        -s

%build

%install
rm -rf %{buildroot}
pear -c pearrc install --nodeps --packagingroot %{buildroot} %{SOURCE0}
        
# Clean up unnecessary files
rm pearrc
rm %{buildroot}/%{peardir}/.filemap
rm %{buildroot}/%{peardir}/.lock
rm -rf %{buildroot}/%{peardir}/.registry
rm -rf %{buildroot}%{peardir}/.channels
rm %{buildroot}%{peardir}/.depdb
rm %{buildroot}%{peardir}/.depdblock



# Install XML package description
mkdir -p %{buildroot}%{xmldir}
tar -xzf %{SOURCE0} package.xml
cp -p package.xml %{buildroot}%{xmldir}/XML_RPC.xml

%clean
rm -rf %{buildroot}

%post
pear install --nodeps --soft --force --register-only %{xmldir}/XML_RPC.xml

%postun
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only pear.php.net/XML_RPC
fi

%files
%defattr(-,root,root)

%{peardir}/*
%{xmldir}/XML_RPC.xml
