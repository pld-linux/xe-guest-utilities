Summary:	daemon for monitoring Xen Virtual machines
Name:		xe-guest-utilities
Version:	7.30.0
Release:	0.0.1
License:	BSD
Source0:	https://github.com/xenserver/xe-guest-utilities/archive/refs/heads/master/%{name}-%{version}-git.tar.gz
# Source0-md5:	77e4b209aac1243ac806920710c5916c
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-recognize-pld.patch
URL:		https://github.com/xenserver/xe-guest-utilities/
BuildRequires:	golang
BuildRequires:	rpmbuild(macros) >= 2.009
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_debugsource_packages	0

%description
xe-daemon for monitoring Virtual Machines on a Xen Hypervisor. Writes
distribution version information, disk and networking statistics to
XenStore.

%prep
%setup -q -n %{name}-master
%patch0 -p1
ln -sf %{_libdir}/golang/src/cmd/vendor/golang.org vendor

%build
%{__make} \
	VENDORDIR=vendor/%{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libexecdir}/%{name}} \
	$RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d} \
	$RPM_BUILD_ROOT{%{systemdunitdir},%{_udevrulesdir}} \
	$RPM_BUILD_ROOT%{_localstatedir}/cache

install -p build/stage%{_sbindir}/* $RPM_BUILD_ROOT%{_sbindir}
install -p build/stage%{_bindir}/* $RPM_BUILD_ROOT%{_libexecdir}/%{name}
install -p mk/xe-linux-distribution.service $RPM_BUILD_ROOT%{systemdunitdir}
install -p mk/xen-vcpu-hotplug.rules $RPM_BUILD_ROOT%{_udevrulesdir}/z10-xen-vcpu-hotplug.rules

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

touch $RPM_BUILD_ROOT%{_localstatedir}/cache/xe-linux-distribution

%post
/sbin/chkconfig --add xe-guest-utilities
%service xe-guest-utilities restart "xe-guest-utilities"
%systemd_reload

%preun
if [ "$1" = "0" ]; then
	%service xe-guest-utilitites stop
	/sbin/chkconfig --del xe-guest-utilitites
fi
%systemd_preun xe-guest-utilitites.service

%postun
%systemd_reload


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CODEOWNERS LICENSE README.md
%attr(755,root,root) %{_sbindir}/xe-daemon
%attr(755,root,root) %{_sbindir}/xe-linux-distribution
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xe-guest-utilities
%{systemdunitdir}/xe-linux-distribution.service
%{_udevrulesdir}/z10-xen-vcpu-hotplug.rules
%{_libexecdir}/xe-guest-utilities
%attr(754,root,root) /etc/rc.d/init.d/xe-guest-utilities
%ghost /var/cache/xe-linux-distribution
