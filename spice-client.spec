
%define tarname spice-client
%define tarversion 0.4.2

%define patchid 18
Name:           spice-client
Version:        0.4.2
Release:        %{patchid}%{?dist}
Summary:        Implements the client side of the SPICE protocol
Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://www.spice-space.org/
Source0:        %{tarname}-%{tarversion}.tar.bz2


patch1: spice-client-01-add-command-line-options.patch
patch2: spice-client-02-fix-dns-lookup.patch
patch3: spice-client-03-add-ipv6-support.patch
patch4: spice-client-04-only-use-AI_ADDRCONF-if-availible.patch
patch5: spice-client-05-new-migration-process.patch
patch6: spice-client-06-fix-handling-of-top-down-images.patch
patch7: spice-client-07-install-spicec-in-usr-libexec.patch
patch8: spice-client-08-add-foreign-menu.patch
patch9: spice-client-09-add-controller.patch
patch10: spice-client-10-fix-controller-foreign-menu-review-comments.patch
patch11: spice-client-11-add-foreign-menu-fix-Makefile.in.patch
patch12: spice-client-12-add-controller-fix-Makefile.in.patch
patch13: spice-client-13-support-for-using-VS2008.patch
patch14: spice-client-14-add-glext_proto-to-Makefile-am.patch
patch15: spice-client-15-x11-fix-a-crash-calling-a-destroyed-window.patch
patch16: spice-client-16-x11-initizlized-sock_len.patch
patch17: spice-client-17-log-warnings-and-errors-to-stderr-too.patch
patch18: spice-client-18-full-screen-do-not-resize-after-migration.patch
patch19: spice-client-19-make-opengl-optional-disabled-by-default.patch
patch20: spice-client-20-fix-unsafe-guest-host-data-handling.patch
patch21: spice-client-21-socket-file.patch

BuildRoot:      %{_tmppath}/%{tarname}-%{version}-%{release}-root-%(%{__id_u} -n)

ExclusiveArch:  i686 x86_64

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  alsa-lib-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXext-devel
BuildRequires:  log4cpp-devel
BuildRequires:  openssl-devel
BuildRequires:  celt051-devel
BuildRequires:  cairo-spice-devel
BuildRequires:  ffmpeg-spice-devel
BuildRequires:  spice-common-devel >= 0.4.2-4

BuildRequires:  autoconf automake libtool


%description
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

This package provides the client side of the SPICE protocol

%prep
%setup -q -n %{tarname}-%{tarversion}

# Note that "patch -p2" is used, as patches are against spice/ and
# not spice/client/.
%patch1 -p2
%patch2 -p2
%patch3 -p2
%patch4 -p2
%patch5 -p2
%patch6 -p2
%patch7 -p2
%patch8 -p2
%patch9 -p2
%patch10 -p2
%patch11 -p2
%patch12 -p2
%patch13 -p2
%patch14 -p2
%patch15 -p2
%patch16 -p2
%patch17 -p2
%patch18 -p2
%patch19 -p2
%patch20 -p2
%patch21 -p1

%build
autoreconf -i -f

CFLAGS="%{optflags}"; CFLAGS="${CFLAGS/-Wall/}"; export CFLAGS;
CXXFLAGS="%{optflags}"; CXXFLAGS="${CXXFLAGS/-Wall/}"; export CXXFLAGS;
FFLAGS="%{optflags}"; FFLAGS="${FFLAGS/-Wall/}"; export FFLAGS;
%configure PATCHID=%{patchid} DISTRIBUTION=%{?dist} --with-spice-common
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root, 0755)
%doc COPYING INSTALL README
%{_libexecdir}/spicec

%changelog
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
