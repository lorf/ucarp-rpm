Summary: Common Address Redundancy Protocol (CARP) for Unix
Name: ucarp
Version: 1.5.2
Release: 16%{?dist}
# See the COPYING file which details everything
License: MIT and BSD
Group: System Environment/Daemons
URL: http://www.ucarp.org/
Source0: ucarp-%{version}.tar
Source1: ucarp.init
Source2: vip-001.conf.example
Source3: vip-common.conf
Source4: vip-up
Source5: vip-down
#Source6: vip-helper.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
BuildRequires: gettext
BuildRequires: autoconf, automake, libtool
BuildRequires: libpcap-devel

%description
UCARP allows a couple of hosts to share common virtual IP addresses in order
to provide automatic failover. It is a portable userland implementation of the
secure and patent-free Common Address Redundancy Protocol (CARP, OpenBSD's
alternative to the patents-bloated VRRP).
Strong points of the CARP protocol are: very low overhead, cryptographically
signed messages, interoperability between different operating systems and no
need for any dedicated extra network link between redundant hosts.


%prep
%setup -q


%build
libtoolize
gettextize -f
cp po/Makevars.template po/Makevars
autoreconf -i
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
%find_lang %{name}

# Install the init script
%{__install} -D -p -m 0755 %{SOURCE1} \
    %{buildroot}/etc/rc.d/init.d/ucarp

%{__mkdir_p} %{buildroot}/etc/ucarp
%{__mkdir_p} %{buildroot}%{_libexecdir}/ucarp

# Install the example config files
%{__install} -D -p -m 0600 %{SOURCE2} %{SOURCE3} \
    %{buildroot}/etc/ucarp/

# Install helper scripts
%{__install} -D -p -m 0700 %{SOURCE4} %{SOURCE5} \
    %{buildroot}%{_libexecdir}/ucarp/


%clean
%{__rm} -rf %{buildroot}


%pre
# Legacy, in case we update from an older package where the service was "carp"
if [ -f /etc/rc.d/init.d/carp ]; then
    /sbin/service carp stop &>/dev/null || :
    /sbin/chkconfig --del carp
fi

%post
/sbin/chkconfig --add ucarp

%preun
if [ $1 -eq 0 ]; then
    /sbin/service ucarp stop &>/dev/null || :
    /sbin/chkconfig --del ucarp
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service ucarp condrestart &>/dev/null || :
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
/etc/rc.d/init.d/ucarp
%attr(0700,root,root) %dir /etc/ucarp/
%config(noreplace) /etc/ucarp/vip-common.conf
/etc/ucarp/vip-001.conf.example
%config(noreplace) %{_libexecdir}/ucarp/
%{_sbindir}/ucarp

%changelog
* Wed Sep 07 2016 James Sumners <james.sumners@gmail.com> - 1.5.2-16
- Fix incorrect logic operator in init file

* Tue Nov 24 2015 James Sumners <james.sumners@gmail.com> - 1.5.2-15
- Build from forked upstream for pidfile support
- Bump version to greater than true EPEL release version

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Apr 28 2010 Jon Ciesla <limb@jcomserv.net> - 1.5.2-1
- New upstream.
- Uses arc4random() if available.
- Avoids adverts that might be twice as what they should be.
- Marked vip-up and vip-down config(noreplace), BZ 586893.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 08 2009 Jon Ciesla <limb@jcomserv.net> - 1.5.1-1
- New upstream.
- New option (--nomcast / -M) to use broadcast 
- advertisements instead of multicast ones.

* Mon Apr 13 2009 Jon Ciesla <limb@jcomserv.net> - 1.5-1
- Update to 1.5 BZ 458767.
- Added LSB header to init script, BZ 247082.
- New upstream should address BZ 427495, 449266, 455394.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb  3 2008 Matthias Saou <http://freshrpms.net/> 1.4-1
- Update to 1.4.
- Rip out all of the "list" stuff and 255.255.255.255 address hack (#427495).
- Change from INITLOG (now deprecated) to LOGGER in the init script.
- Move helper scripts to /usr/libexec/ucarp/.

* Thu Aug 23 2007 Matthias Saou <http://freshrpms.net/> 1.2-9
- Rebuild for new BuildID feature.

* Sun Aug  5 2007 Matthias Saou <http://freshrpms.net/> 1.2-8
- Update License field.

* Fri Feb  2 2007 Matthias Saou <http://freshrpms.net/> 1.2-7
- Rename service from carp to ucarp, to be more consistent.
- Move /etc/sysconfig/carp to /etc/ucarp since it has become a config directory
  of its own.

* Wed Nov 29 2006 Matthias Saou <http://freshrpms.net/> 1.2-6
- Rebuild against new libpcap.

* Mon Nov 13 2006 Matthias Saou <http://freshrpms.net/> 1.2-5
- Include all improvements from Denis Ovsienko (#200395).

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 1.2-4
- FC6 rebuild.

* Tue Aug 22 2006 Matthias Saou <http://freshrpms.net/> 1.2-3
- Update to 1.3 snapshot, which includes the ARP fix, as well as fixes for the
  segfaults reported in #200400 and #201596.
- Add autoconf, automake and libtool build reqs for the 1.3 patch.

* Thu Jul 27 2006 Matthias Saou <http://freshrpms.net/> 1.2-3
- Fix init script for recent find versions (#200395).

* Thu Jun 22 2006 Matthias Saou <http://freshrpms.net/> 1.2-2
- Include ARP patch backported from 1.3 snapshot (#196095).
- Make libpcap build requirement conditional to be able to share spec file.

* Wed Jun 21 2006 Matthias Saou <http://freshrpms.net/> 1.2-1
- Update to 1.2.
- BuildRequire libpcap-devel instead of libpcap now that it has been split.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 1.1-5
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 1.1-4
- Rebuild for new gcc/glibc.

* Thu Nov 17 2005 Matthias Saou <http://freshrpms.net/> 1.1-3
- Rebuild against new libpcap library.

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.1-2
- Add %%dir entry for /etc/sysconfig/carp directory.

* Thu Jan 13 2005 Matthias Saou <http://freshrpms.net/> 1.1-1
- Update to 1.1.
- Update source location.

* Fri Jul  9 2004 Matthias Saou <http://freshrpms.net/> 1.0-1
- Initial RPM release.

