#
Summary:	Camera lens database with image correction support
Summary(pl.UTF-8):	Baza danych obiektywów z funkcją korekcji zdjęć
Name:		lensfun
Version:	0.2.3
Release:	0.1
License:	LGPL
Group:		Libraries
Source0:	http://download.berlios.de/lensfun/%{name}-%{version}.tar.bz2
URL:		http://developer.berlios.de/projects/lensfun/
BuildRequires:	make >= 3.81
#BuildRequires:	xorg-util-gccmakedep >= 1.0.2
BuildRequires:	doxygen >= 1.5.0
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	libpng >= 1.0
BuildRequires:	zlib
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
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
lensfun library header files.

%description -l pl.UTF-8 devel
Pliki nagłówkowe biblioteki lensfun.

%package apidocs
Summary:	lensfun library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki lensfun
Group:		Documentation

%description apidocs
lensfun library API documentation.

%description -l pl.UTF-8 apidocs
Dokumentacja API biblioteki lensfun.

%prep
%setup -q

%build
./configure --prefix=%{_prefix}

# TODO:
# Can't use:
# LDFLAGS="%{rpmldflags}" \
# It doesn't work.
# 
# Command
# make CFLAGS=-O2 -fno-strict-aliasing -fwrapv -march=i686 -mtune=pentium4 -gdwarf-2 -g2  all
# works OK
#
# Command
# make CFLAGS=-O2 -fno-strict-aliasing -fwrapv -march=i686 -mtune=pentium4 -gdwarf-2 -g2  LDFLAGS=-Wl,--as-needed -Wl,-z,relro -Wl,-z,-combreloc  all
# gives a lot of errors such as:
# out/posix/release/liblensfun.so: undefined reference to `g_markup_error_quark

%{__make} \
	CFLAGS="%{rpmcflags}" \
	all

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# TODO:
# The link "liblensfun.so" as created by build process points to "liblensfun.so.0".
# This creates dependency "lensfun-devel requires /usr/lib/liblensfun.so.0".
# But liblensfun.so.0 is created in %post script by ldconfig and such requirement
# can not be satisfied.
(
	cd $RPM_BUILD_ROOT/%{_libdir}
	ln -sf liblensfun.so.*.*.* liblensfun.so
)

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%{_libdir}/liblensfun.so.*.*.*
%{_datadir}/lensfun

%files devel
%defattr(644,root,root,755)
%{_includedir}/lensfun.h
%{_libdir}/liblensfun.so
%{_pkgconfigdir}/lensfun.pc

%files apidocs
%defattr(644,root,root,755)
