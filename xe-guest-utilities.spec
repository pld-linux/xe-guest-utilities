Summary:	daemon for monitoring Xen Virtual machines
Name:		xe-guest-utilities
Version:	7.30.0
Release:	0.0.1
License:	BSD
Source0:	https://github.com/xenserver/xe-guest-utilities/archive/refs/heads/master/%{name}-%{version}-git.tar.gz
# Source0-md5:	77e4b209aac1243ac806920710c5916c
URL:		https://github.com/xenserver/xe-guest-utilities/
BuildRequires:	golang
BuildRequires:	rpmbuild(macros) >= 2.009
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_debugsource_packages	0

%description
xe-daemon for monitoring Virtual Machines on a Xen Hypervisor.
Writes distribution version information, disk and networking
statistics to XenStore.

%prep
%setup -q -n %{name}-master
ln -sf %{_libdir}/golang/src/cmd/vendor/golang.org vendor

%build
%{__make} \
	VENDORDIR=vendor/%{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
mv -v build/stage%{_sbindir}/* $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_libexecdir}/%{name}
mv -v build/stage%{_bindir}/* $RPM_BUILD_ROOT%{_libexecdir}/%{name}

install -d $RPM_BUILD_ROOT%{systemdunitdir}
cp -p mk/xe-linux-distribution.service $RPM_BUILD_ROOT%{systemdunitdir}
install -d $RPM_BUILD_ROOT%{_udevrulesdir}
cp -p mk/xen-vcpu-hotplug.rules $RPM_BUILD_ROOT%{_udevrulesdir}/z10-xen-vcpu-hotplug.rules

install -d $RPM_BUILD_ROOT%{_localstatedir}/cache
touch $RPM_BUILD_ROOT%{_localstatedir}/cache/xe-linux-distribution

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_sbindir}/xe-daemon
%attr(755,root,root) %{_sbindir}/xe-linux-distribution
%{systemdunitdir}/xe-linux-distribution.service
%{_udevrulesdir}/z10-xen-vcpu-hotplug.rules
%{_libexecdir}/xe-guest-utilities
#%%ghost /var/cache/xe-linux-distribution
