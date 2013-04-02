Name:           spice-client
Version:        0.6.3
# We started at 3 for RHEL-6.1, 2%{?dist}.x is for RHEL-6.0.z, 1 is for RHEL-5
Release:        2%{?dist}.5
Summary:        Implements the client side of the SPICE protocol
Group:          User Interface/Desktops
License:        LGPLv2+
URL:            http://www.spice-space.org/
Source0:        http://www.spice-space.org/download/releases/spice-%{version}.tar.bz2
Source1:        http://www.spice-space.org/download/releases/spice-protocol-%{version}.tar.bz2
Patch0:         0001-spicec-x11-Change-source-of-controller-socket-name-f.patch
Patch1:         0002-client-Interpret-the-title-control-message-as-utf8-i.patch
Patch2:         0003-Remove-no-longer-used-wstring_printf-functions.patch
Patch3:         0004-spicec-x11-Do-not-set-_NET_WM_USER_TIME-to-0-on-star.patch
Patch4:         0005-spicec-Fix-info-layer-sometimes-not-showing.patch
Patch5:         0006-spicec-x11-Add-a-few-missing-XLockDisplay-calls-rhbz.patch
Patch6:         0007-spicec-x11-Fix-modifier-keys-getting-stuck-rhbz-6550.patch
Patch7:         0008-spicec-x11-Fix-unhandled-exception-no-window-proc-cr.patch
Patch8:         0009-spicec-Don-t-show-a-white-screen-if-guest-resolution.patch
BuildRoot:      %{_tmppath}/%{tarname}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:  i686 x86_64
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  alsa-lib-devel
BuildRequires:  pixman-devel >= 0.18
BuildRequires:  libjpeg-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXext-devel
BuildRequires:  libXfixes-devel
BuildRequires:  openssl-devel
BuildRequires:  celt051-devel
Requires:       pixman >= 0.18

%description
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

This package provides the client side of the SPICE protocol


%prep
%setup -q -n spice-%{version} -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1


%build
# generate spice-protocol.pc, to make spice configure happy
pushd spice-protocol-%{version}
./configure
popd
export CFLAGS="%{optflags} -I$(pwd)/spice-protocol-%{version}"
export CXXFLAGS="%{optflags} -I$(pwd)/spice-protocol-%{version}"
export PKG_CONFIG_PATH=$(pwd)/spice-protocol-%{version}
%configure
make -C client %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make -C client install DESTDIR=$RPM_BUILD_ROOT
# create libexec 0.4 compat link
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
ln -s %{_bindir}/spicec $RPM_BUILD_ROOT%{_libexecdir}/spicec


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{_bindir}/spicec
%{_libexecdir}/spicec


%changelog
* Thu Nov 25 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-2.el6_0.5
- Add fixes from upstream git for a number of serious bugs:
  - ctrl / alt getting stuck
  - a client hang
  - a client crash
  - showing nothing but a white screen in fullscreen mode
  Related: rhbz#644840

* Tue Nov 16 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-2.el6_0.4
- Add explicit Requires for pixman >= 0.18
  Related: rhbz#644840

* Tue Nov  9 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-2.el6_0.3
- Fix the watermark and sticky key notifications not being shown
  Related: rhbz#644840

* Thu Oct 21 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-2.el6_0.2
- Fix the spicec window not being on top when first shown
  Related: rhbz#644840

* Thu Oct 21 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-2.el6_0.1
- New upstream release 0.6.3
- Fix setting window title from xpi
  Resolves: rhbz#644840

* Wed Aug 4 2010 Martin Stransky <stransky@redhat.com> - 0.4.2-18
- fix spice-xpi/qspice-client unix socket race
  Resolves: #620444

* Fri Jul 30 2010 Uri Lublin <uril@redhat.com> - 0.4.2-17
 - fix unsafe guest/host data handling
 Resolves: #568811

* Tue Jun 29 2010 Uri Lublin <uril@redhat.com> - 0.4.2-16
- remove BuildRequires mesa-libGLU-devel
  + open-gl is now disabled.
Related: #482556

* Tue Jun 29 2010 Uri Lublin <uril@redhat.com> - 0.4.2-15
 - make opengl optional, disabled by default
Resolves: #482556

* Tue Jun 29 2010 Uri Lublin <uril@redhat.com> - 0.4.2-14
 - client: spicec --full-screen=auto-conf do not resize after migration
Resolves: #584318

* Tue Jun 29 2010 Uri Lublin <uril@redhat.com> - 0.4.2-13
 - client: log warnings and errors to stderr too
Resolves: #580925

* Mon Jun 21 2010 Uri Lublin <uril@redhat.com> - 0.4.2-12
 - client: x11: call getsockname() with initizlized sock_len
 Resolves: #604701

* Sun Apr  4 2010 Uri Lublin <uril@redhat.com> - 0.4.2-11
 - client: x11: fix a crash caused by a call to a destroyed window
Resolves: #578458

* Sun Apr  4 2010 Uri Lublin <uril@redhat.com> - 0.4.2-10
 - Add glext_proto.h file to client/Makefile.am
Related: #576639

* Sun Apr  4 2010 Uri Lublin <uril@redhat.com> - 0.4.2-9
 - generate auto* generated files (e.g. Makefile.in)
Resolves: #579328

* Wed Mar 24 2010 Uri Lublin <uril@redhat.com> - 0.4.2-8
 - support for building windows client using VS2008
 - also fixed a typo in 0.4.2-7
Resolves: #576639

* Tue Mar 23 2010 Uri Lublin <uril@redhat.com> - 0.4.2-7
 - spice: client: add foreign menu
 - spice: client: add controller
 - spice: client: fix controller & foreign menu review comments
Resolves: #558248
Resolves: #558247

* Tue Mar 23 2010 Uri Lublin <uril@redhat.com> - 0.4.2-6
 - spice: client: x11: install spicec in /usr/libexec
Resolves: #576437

* Tue Mar 23 2010 Uri Lublin <uril@redhat.com> - 0.4.2-5
 - fix handling of top down images in video streams
Resolves: #576151

* Tue Mar 23 2010 Uri Lublin <uril@redhat.com> - 0.4.2-4
 - new migration process
Resolves: #576031

* Thu Mar 18 2010 Uri Lublin <uril@redhat.com> - 0.4.2-3
- fix dns lookup
- enable ipv6
Resolves: #566444

* Thu Mar 18 2010 Uri Lublin <uril@redhat.com> - 0.4.2-2
- add command line support for ciphers, ca file, and host certificate subject
Resolves: #573371

* Mon Mar  1 2010 Uri Lublin <uril@redhat.com> - 0.4.2-1
 - This package does not "Requires: pkgconfig" (removed).
Related: #543948

* Mon Jan 11 2009 Uri Lublin <uril@redhat.com> - 0.4.2-0
 - first spec for 0.4.2
Related: #549814
