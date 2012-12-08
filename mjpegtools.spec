%define api 2.0
%define major 0
%define libname %mklibname %{name}%{api}_ %{major}
%define develname %mklibname -d %{name}

Name:		mjpegtools
Version:	2.0.0
Release:	4
Summary:	Tools for recording, editing, playing back and mpeg-encoding video under linux
License:	GPLv2+
Group:		Video
Url:		http://mjpeg.sourceforge.net
Source: 	http://prdownloads.sourceforge.net/mjpeg/%{name}-%{version}.tar.gz
Patch0:		mjpegtools-2.0.0-format-strings.patch
Patch1: 	mjpegtools-1.9.0rc1-x86_64.patch
Patch4:		mjpegtools-1.9.0-link.patch
BuildRequires:	autoconf
BuildRequires:	nasm
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(SDL_gfx)
BuildRequires:	pkgconfig(xxf86dga)
BuildRequires:	pkgconfig(libquicktime)
Buildrequires:	pkgconfig(libdv)
BuildRequires:	pkgconfig(libpulse)
Requires:	%{libname} = %{version}-%{release}

%description
The MJPEG-tools are a basic set of utilities for recording, editing, 
playing back and encoding (to mpeg) video under linux. Recording can
be done with zoran-based MJPEG-boards (LML33, Iomega Buz, Pinnacle
DC10(+), Marvel G200/G400), these can also playback video using the
hardware. With the rest of the tools, this video can be edited and
encoded into mpeg1/2 or divx video.

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	libmjpegtools = %{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n	%{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q
%patch0 -p1 -b .format-strings
%patch1 -p1
%patch4 -p0

libtoolize --copy --force
autoreconf
# toolame isn't in Mandriva, mp2enc is, so use that
perl -p -i -e 's/\-\"toolame\"/\-\"mp2enc\"/g' scripts/lav2mpeg

%build
export CPPFLAGS="%{optflags} -fpermissive"
export CFLAGS="%{optflags}"
export PTHREAD_LIBS="-lpthread"

# build i686/mmx dynamic library
%ifarch %{ix86}
mkdir build-i686
pushd build-i686
CONFIGURE_TOP=.. %configure2_5x \
	--enable-simd-accel \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--without-v4l \
	--disable-static

make
popd
%endif

# build regular package
%if %{_target_cpu} == "i686"
%else
mkdir build-%{_target_cpu}
%endif

pushd build-%{_target_cpu}
CONFIGURE_TOP=.. %configure2_5x \
	--disable-simd-accel \
	--libdir=%{_libdir} \
	--without-v4l \
	--disable-static

make
popd

%install
%ifarch %{ix86}
pushd build-i686
%makeinstall_std
popd
mkdir -p %{buildroot}%{_libdir}/sse2
mv %{buildroot}%{_libdir}/*.so.* %{buildroot}%{_libdir}/sse2/
%endif

pushd build-%{_target_cpu}
%makeinstall_std
popd

cp mpeg2enc/mpeg2syntaxcodes.h %{buildroot}%{_includedir}/mjpegtools/

%files
%doc AUTHORS BUGS ChangeLog CHANGES COPYING HINTS INSTALL NEWS PLANS README* TODO
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/mjpeg-howto.info*

%files -n %{libname}
%{_libdir}/lib*-%{api}.so.%{major}*
%ifarch %{ix86}
%{_libdir}/sse2/lib*-%{api}.so.%{major}*
%endif

%files -n %{develname}
%{_mandir}/man5/yuv4mpeg.5*
%{_includedir}/mjpegtools
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%changelog
* Tue May 24 2011 GÃ¶tz Waschk <waschk@mandriva.org> 2.0.0-3mdv2011.0
+ Revision: 678151
- fix devel obsoletes

* Tue May 24 2011 GÃ¶tz Waschk <waschk@mandriva.org> 2.0.0-2
+ Revision: 678126
- fix devel name and obsolete old package

* Tue May 24 2011 GÃ¶tz Waschk <waschk@mandriva.org> 2.0.0-1
+ Revision: 678106
- new version
- new major
- update licens
- rediff patch 0
- drop patches 2,3

* Fri May 06 2011 Funda Wang <fwang@mandriva.org> 1.9.0-10
+ Revision: 669946
- fix build

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Fri Dec 17 2010 Funda Wang <fwang@mandriva.org> 1.9.0-9mdv2011.0
+ Revision: 622484
- rebuild for new directfb

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.9.0-8mdv2011.0
+ Revision: 606647
- rebuild

* Wed Feb 03 2010 Thierry Vignaud <tv@mandriva.org> 1.9.0-7mdv2010.1
+ Revision: 500387
- typo fix in summary (Dimitrios Glentadakis)

* Mon Jan 25 2010 Oden Eriksson <oeriksson@mandriva.com> 1.9.0-6mdv2010.1
+ Revision: 496056
- fix #55450 (jpeg2yuv segfaults with libjpeg7)

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.9.0-5mdv2010.1
+ Revision: 488788
- rebuilt against libjpeg v8

* Sun Nov 08 2009 Funda Wang <fwang@mandriva.org> 1.9.0-4mdv2010.1
+ Revision: 463087
- rebuild for new dfb

* Sun Sep 27 2009 Funda Wang <fwang@mandriva.org> 1.9.0-3mdv2010.0
+ Revision: 449968
- rebuild for new SDL_gfx

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 1.9.0-2mdv2010.0
+ Revision: 416628
- rebuilt against libjpeg v7

* Tue Jan 06 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1.9.0-1mdv2009.1
+ Revision: 325574
- new version
- fix format strings
- drop patch 3
- call libtoolize
- remove old configure options

* Mon Dec 08 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1.9.0-0.rc4.1mdv2009.1
+ Revision: 311863
- new version
- drop patch 4
- fix build

* Mon Jun 09 2008 Pixel <pixel@mandriva.com> 1.9.0-0.rc3.3mdv2009.1
+ Revision: 217193
- do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri May 30 2008 Funda Wang <fwang@mandriva.org> 1.9.0-0.rc3.3mdv2009.0
+ Revision: 213563
- disable no_undefined, otherwise it will fail itself
- drop old conditions
- add gentoo patch for gcc 4.3

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Dec 05 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.9.0-0.rc3.1mdv2008.1
+ Revision: 115622
- new version

* Wed Sep 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.9.0-0.rc2.4mdv2008.1
+ Revision: 89943
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - s/Mandrake/Mandriva/

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - remove obsolete patch

* Wed Jun 06 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 1.9.0-0.rc2.3mdv2008.0
+ Revision: 36104
- Rebuild with libslang2.

* Tue May 22 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.9.0-0.rc2.2mdv2008.0
+ Revision: 29632
- rebuild

* Wed Apr 18 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.9.0-0.rc2.1mdv2008.0
+ Revision: 14732
- new version
- new major
- drop patch 1
- patch 2: fix build on x86_64


* Mon Jun 19 2006 Götz Waschk <waschk@mandriva.org> 1.8.0-4mdv2007.0
- build with -fpermissive

* Mon Apr 03 2006 Götz Waschk <waschk@mandriva.org> 1.8.0-3mdk
- move optimized i686 libs to sse2 dir

* Wed Mar 08 2006 Götz Waschk <waschk@mandriva.org> 1.8.0-2mdk
- patch to make it build with new libquicktime

* Tue Oct 04 2005 Götz Waschk <waschk@mandriva.org> 1.8.0-1mdk
- new version

* Mon Sep 05 2005 Götz Waschk <waschk@mandriva.org> 1.6.3-0.rc3.3mdk
- rebuild trying to fix #18242

* Sun Aug 28 2005 Götz Waschk <waschk@mandriva.org> 1.6.3-0.rc3.2mdk
- reenable fortify

* Sat Aug 27 2005 Götz Waschk <waschk@mandriva.org> 1.6.3-0.rc3.1mdk
- disable fortify to make it build
- new version

* Fri Aug 12 2005 Götz Waschk <waschk@mandriva.org> 1.6.3-0.rc2.1mdk
- new major
- new version

* Thu May 26 2005 Götz Waschk <waschk@mandriva.org> 1.6.3-0.rc1.2mdk
- add missing header

* Tue May 24 2005 Götz Waschk <waschk@mandriva.org> 1.6.3-0.rc1.1mdk
- mkrel
- update file list
- fix optimization flags
- fix buildrequires
- drop patches 1,2,4,5
- new version

* Wed Feb 09 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.6.2-10mdk
- lib64 / multiarch

* Sun Jan 30 2005 Austin Acton <austin@mandrake.org> 1.6.2-9mdk
- patch for new quicktime

* Fri Nov 12 2004 Götz Waschk <waschk@linux-mandrake.com> 1.6.2-8mdk
- drop 9.0 support

* Tue Jun 29 2004 Austin Acton <austin@mandrake.org> 1.6.2-7mdk
- from Marc Koschewski <marc@osknowledge.org> :
  - fix i686 build

* Tue Jun 15 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.6.2-6mdk
- buildrequires
- reenable libtoolize
- no .bz2 ending of man pages in %%files list
- cosmetics

* Mon Jun 14 2004 Götz Waschk <waschk@linux-mandrake.com> 1.6.2-5mdk
- fix cflags for i686
- patch for new g++

* Thu May 13 2004 Götz Waschk <waschk@linux-mandrake.com> 1.6.2-4mdk
- build with libquicktime

* Thu May 13 2004 Götz Waschk <waschk@linux-mandrake.com> 1.6.2-3mdk
- build static libs with -fPIC as they may be linked into a DSO

* Fri Apr 02 2004 Götz Waschk <waschk@linux-mandrake.com> 1.6.2-2mdk
- new libdv

* Fri Apr 02 2004 Götz Waschk <waschk@linux-mandrake.com> 1.6.2-1mdk
- new version

* Wed Mar 17 2004 Götz Waschk <waschk@linux-mandrake.com> 1.6.1.93-3mdk
- build with SDL for yuvplay

* Sun Jan 18 2004 Götz Waschk <waschk@linux-mandrake.com> 1.6.1.93-2mdk
- patch to add info dir entry

* Sat Jan 17 2004 Götz Waschk <waschk@linux-mandrake.com> 1.6.1.93-1mdk
- use mdkversion macro
- new version

* Thu Nov 27 2003 Götz Waschk <waschk@linux-mandrake.com> 1.6.1.92-1mdk
- new version

* Tue Nov 25 2003 Götz Waschk <waschk@linux-mandrake.com> 1.6.1.91-1mdk
- fix file list
- no parallel build, please 
- drop patch 4
- new version

* Wed Nov 05 2003 Götz Waschk <waschk@linux-mandrake.com> 1.6.1.90-2mdk
- fix buildrequires

* Tue Nov 04 2003 Götz Waschk <waschk@linux-mandrake.com> 1.6.1.90-1mdk
- rediff patch 3
- clean buildroot before installation
- add new files
- don't libtoolize
- patch4: fix illegal libtool version number
- use YV12 option
- drop patches 0,1,2
- don't require avifile anymore
- new version

* Sat Oct 25 2003 Stefan van der Eijk <stefan@eijk.nu> 1.6.1-11mdk
- BuildRequires

* Tue Oct 21 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.6.1-10mdk
- libtool fixes

* Tue Sep 02 2003 Götz Waschk <waschk@linux-mandrake.com> 1.6.1-9mdk
- fix buildrequires

* Mon Jul 21 2003 Götz Waschk <waschk@linux-mandrake.com> 1.6.1-8mdk
- patch2: disable werror to make it build
- patch1: fix avifile header location

* Wed Jul 09 2003 Götz Waschk <waschk@linux-mandrake.com> 1.6.1-7mdk
- autoconf2.5 macro for the non-686 version

