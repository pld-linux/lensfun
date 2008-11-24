#
Summary:	Camera lens database with image correction support
Summary(pl.UTF-8):	Baza danych obiektywów z funkcją korekcji zdjęć
Name:		lensfun
Version:	0.2.3
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://download.berlios.de/lensfun/%{name}-%{version}.tar.bz2
# Source0-md5:	c5c04be4f53e3eef450ff4948d8f65b3
URL:		http://developer.berlios.de/projects/lensfun/
Patch0:		%{name}-build.patch
BuildRequires:	doxygen >= 1.5.0
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	libpng >= 1.0
BuildRequires:	libstdc++-devel
BuildRequires:	make >= 3.81
BuildRequires:	python
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The project provides a database of photographic lenses and a library
that allows advanced access to the database including functions to
correct images based on intimate knowledge of lens characteristics and
calibration data.

%description -l pl.UTF-8
Projekt dostarcza bazę danych obiektywów oraz bibliotekę pozwalającą
na dstęp do bazy i dodatkowo oferującą korekcję zdjęć w oparciu o
szczegółową charakterystykę obiektywu.

%package devel
Summary:	lensfun library header files
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki lensfun
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
lensfun library header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki lensfun.

%package apidocs
Summary:	lensfun library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki lensfun
Group:		Documentation

%description apidocs
lensfun library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki lensfun.

%prep
%setup -q
%patch0 -p1

%build
# configure is a python application which tries to mimic autoconf
CC="%{__cc}" \
CXX="%{__cxx}" \
LD="%{__cxx}" \
./configure \
 	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--sysconfdir=%{_sysconfdir} \
	--datadir=%{_datadir}/%{name} \
	--libdir=%{_libdir} \
	--includedir=%{_includedir} \
	--libexecdir=%{_libexecdir} \
	--cflags="%{rpmcflags}" \
	--cxxflags="%{rpmcxxflags}" \
 	--ldflags="%{rpmldflags}" \
	--compiler="gcc"

# 'all' is not the default target
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/liblensfun.so.*.*.*
%{_datadir}/lensfun

%files devel
%defattr(644,root,root,755)
%{_includedir}/lensfun.h
%{_libdir}/liblensfun.so
%{_pkgconfigdir}/lensfun.pc

%files apidocs
%defattr(644,root,root,755)
