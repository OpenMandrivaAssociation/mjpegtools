%define name	mjpegtools
%define version	1.9.0
%define prerel rc3
%define rel 0.%prerel.3
%define release %mkrel %rel
%define api	1.9
%define major 0
%define libname %mklibname %name%{api}_ %major
%define filename %name-%version%prerel
#fixed2
%{?!mkrel:%define mkrel(c:) %{-c: 0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*\\D\+)?(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{?distversion:%distversion}%{?!distversion:%(echo $[%{mdkversion}/10])}}%{?_with_unstable:%{1}}%{?distsuffix:%distsuffix}%{?!distsuffix:mdk}}

%define _disable_ld_no_undefined 1
Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Tools for recording, editing, playing back and mpeg-encoding video under linux
License:	GPL
Url:		http://mjpeg.sourceforge.net
Group:		Video
Source: 	http://prdownloads.sourceforge.net/mjpeg/%{filename}.tar.gz
Patch2: 	mjpegtools-1.9.0rc1-x86_64.patch
Patch3: 	mjpegtools-1.6.1.90-libtool.patch
Patch4:		mjpegtools-1.9.0_rc3-gcc43.patch
Requires:	%{libname} = %{version}
BuildRequires:  autoconf2.5
BuildRequires:  gtk+2-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libSDL_gfx-devel
BuildRequires:  libxxf86dga-devel
BuildRequires:  libquicktime-devel nasm
Buildrequires:	libdv-devel >= 0.99
BuildRequires:	pulseaudio-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The MJPEG-tools are a basic set of utilities for recording, editing, 
playing back and encoding (to mpeg) video under linux. Recording can
be done with zoran-based MJPEG-boards (LML33, Iomega Buz, Pinnacle
DC10(+), Marvel G200/G400), these can also playback video using the
hardware. With the rest of the tools, this video can be edited and
encoded into mpeg1/2 or divx video.

%package -n	%{libname}
Summary:	Main library for for %{name}
Group:		System/Libraries
Provides:	libmjpegtools = %version-%release
Obsoletes:	libmjpegtools0 < %version-%release

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{libname}-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %version-%release
Obsoletes:	libmjpegtools0-devel < %version-%release

%description -n	%{libname}-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q -n %filename
%patch2 -p1
%patch3 -p1 -b .libtool
%patch4 -p1
autoconf
# toolame isn't in Mandriva, mp2enc is, so use that
perl -p -i -e 's/\-\"toolame\"/\-\"mp2enc\"/g' scripts/lav2mpeg

%build
export CPPFLAGS="%{optflags} -fpermissive -pthread"
export CFLAGS="%{optflags} -fpermissive -pthread"
# build i686/mmx dynamic library
%ifarch %{ix86}
mkdir build-i686
pushd build-i686
CONFIGURE_TOP=.. ../configure --enable-cmov-extension --enable-simd-accel \
  --libdir=%_libdir --with-dv-yv12
make
popd
%endif
# build regular package

%if %{_target_cpu} == "i686"
%else
mkdir build-%{_target_cpu}
%endif

pushd build-%{_target_cpu}
CONFIGURE_TOP=.. %configure2_5x --disable-cmov-extension --disable-simd-accel \
  --libdir=%_libdir --with-dv-yv12
make
popd

%install
rm -rf %buildroot
%ifarch %{ix86}
pushd build-i686
%makeinstall
popd
mkdir -p $RPM_BUILD_ROOT/%_libdir/sse2
mv $RPM_BUILD_ROOT/%_libdir/*.so.* $RPM_BUILD_ROOT/%_libdir/sse2
%endif
pushd build-%{_target_cpu}
%makeinstall
popd
cp mpeg2enc/mpeg2syntaxcodes.h %buildroot%_includedir/mjpegtools/

%post
%_install_info mjpeg-howto.info

%postun
%_remove_install_info mjpeg-howto.info


%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig 
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog CHANGES COPYING HINTS INSTALL NEWS PLANS README* TODO
%_bindir/*
%{_mandir}/man1/*
%_infodir/mjpeg-howto.info*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*-%api.so.%{major}*
%ifarch %{ix86}
%{_libdir}/sse2/lib*-%api.so.%{major}*
%endif

%files -n %{libname}-devel
%defattr(-,root,root)
%_mandir/man5/yuv4mpeg.5*
%{_includedir}/mjpegtools
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.la

