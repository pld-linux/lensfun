Summary:	Camera lens database with image correction support
Summary(pl.UTF-8):	Baza danych obiektywów z funkcją korekcji zdjęć
Name:		lensfun
Version:	0.3.0
Release:	1
License:	LGPL v3 (library), CC-BY-SA v3.0 (lens database)
Group:		Libraries
Source0:	http://downloads.sourceforge.net/lensfun/%{name}-%{version}.tar.bz2
# Source0-md5:	c553cb37f1b781d1af05787beacf0193
Patch0:		FHS.patch
URL:		http://lensfun.sourceforge.net/
BuildRequires:	cmake >= 2.8
BuildRequires:	docutils
BuildRequires:	doxygen >= 1.5.0
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	libpng-devel >= 1.0
BuildRequires:	libstdc++-devel
BuildRequires:	make >= 3.81
BuildRequires:	pkgconfig
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

%package apidocs
Summary:	lensfun API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki lensfun
Group:		Documentation

%description apidocs
lensfun API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki lensfun.

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

# packaged as %doc in -apidocs
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README docs/{adobe-lens-profile,cc-by-sa-3.0,manual-main,mounts}.txt
%attr(755,root,root) %{_libdir}/libauxfun.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libauxfun.so.0
%attr(755,root,root) %{_libdir}/liblensfun.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblensfun.so.0
%attr(755,root,root) %{_bindir}/g-lensfun-update-data
%attr(755,root,root) %{_bindir}/lensfun-add-adapter
%attr(755,root,root) %{_bindir}/lensfun-update-data
%{_mandir}/man1/g-lensfun-update-data.1*
%{_mandir}/man1/lensfun-add-adapter.1*
%{_mandir}/man1/lensfun-update-data.1*
%{_datadir}/lensfun

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libauxfun.so
%attr(755,root,root) %{_libdir}/liblensfun.so
%{_includedir}/auxfun
%{_includedir}/lensfun
%{_pkgconfigdir}/lensfun.pc

%files apidocs
%defattr(644,root,root,755)
%doc build/doc_doxygen/*
