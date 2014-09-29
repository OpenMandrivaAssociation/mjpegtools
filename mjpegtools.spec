%define api 2.1
%define major 0
%define libname %mklibname %{name} %{api} %{major}
%define devname %mklibname -d %{name}

Summary:	Tools for recording, editing, playing back and mpeg-encoding video under linux
Name:		mjpegtools
Version:	2.1.0
Release:	1
License:	GPLv2+
Group:		Video
Url:		http://mjpeg.sourceforge.net
Source0: 	http://prdownloads.sourceforge.net/mjpeg/%{name}-%{version}.tar.gz
Patch0:		mjpegtools-2.1.0-format-strings.patch
Patch1: 	mjpegtools-1.9.0rc1-x86_64.patch
Patch4:		mjpegtools-1.9.0-link.patch
BuildRequires:	nasm
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(gtk+-2.0)
Buildrequires:	pkgconfig(libdv)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libquicktime)
BuildRequires:	pkgconfig(SDL_gfx)
BuildRequires:	pkgconfig(xxf86dga)

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

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q
%apply_patches

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
CONFIGURE_TOP=.. %configure \
	--enable-simd-accel \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--without-v4l \
	--disable-static

%make
popd
%endif

# build regular package
%if "%{_target_cpu}" == "i686"
%else
mkdir build-%{_target_cpu}
%endif

pushd build-%{_target_cpu}
CONFIGURE_TOP=.. %configure \
	--disable-simd-accel \
	--libdir=%{_libdir} \
	--without-v4l \
	--disable-static

%make
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

%files -n %{devname}
%{_mandir}/man5/yuv4mpeg.5*
%{_includedir}/mjpegtools
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
