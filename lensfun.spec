Summary:	Camera lens database with image correction support
Summary(pl.UTF-8):	Baza danych obiektywów z funkcją korekcji zdjęć
Name:		lensfun
Version:	0.2.7
Release:	1
License:	LGPL v3 (library), CC-BY-SA v3.0 (lens database)
Group:		Libraries
Source0:	http://download.berlios.de/lensfun/%{name}-%{version}.tar.bz2
# Source0-md5:	6061cc2d00a42d3e62512878426fc841
Patch0:		%{name}-auxfun.patch
URL:		http://developer.berlios.de/projects/lensfun/
BuildRequires:	cmake >= 2.8
BuildRequires:	doxygen >= 1.5.0
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	libpng-devel >= 1.0
BuildRequires:	libstdc++-devel
BuildRequires:	make >= 3.81
BuildRequires:	python
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	zlib-devel >= 1.0
Obsoletes:	lensfun-apidocs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The project provides a database of photographic lenses and a library
that allows advanced access to the database including functions to
correct images based on intimate knowledge of lens characteristics and
calibration data.

%description -l pl.UTF-8
Projekt dostarcza bazę danych obiektywów oraz bibliotekę pozwalającą
na dostęp do bazy i dodatkowo oferującą korekcję zdjęć w oparciu o
szczegółową charakterystykę obiektywu.

%package devel
Summary:	lensfun library header files
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki lensfun
License:	LGPL v3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
lensfun library header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki lensfun.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DBUILD_AUXFUN:BOOL=ON \
	-DBUILD_DOC:BOOL=ON \
	-DBUILD_TESTS:BOOL=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install/fast \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README docs/cc-by-sa-3.0.txt
%attr(755,root,root) %{_libdir}/libauxfun.so.*.*.*.*
%attr(755,root,root) %{_libdir}/liblensfun.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblensfun.so.0
%{_datadir}/lensfun

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libauxfun.so
%attr(755,root,root) %{_libdir}/liblensfun.so
%{_includedir}/auxfun
%{_includedir}/lensfun
%{_pkgconfigdir}/lensfun.pc
