#
# Conditional build:
%bcond_with	sse		# SSE instructions
%bcond_with	sse2		# SSE2 instructions

%ifarch pentium3 pentium4 %{x8664} x32
%define	with_sse	1
%endif
%ifarch pentium4 %{x8664} x32
%define	with_sse2	1
%endif

Summary:	Camera lens database with image correction support
Summary(pl.UTF-8):	Baza danych obiektywów z funkcją korekcji zdjęć
Name:		lensfun
Version:	0.3.3
Release:	1
License:	LGPL v3 (library), CC-BY-SA v3.0 (lens database)
Group:		Libraries
#Source0Download: https://github.com/lensfun/lensfun/releases
Source0:	https://github.com/lensfun/lensfun/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	04e0b58fd685ee680b0d70d61f0a5c17
Patch0:		%{name}-regex-lock.patch
URL:		http://lensfun.sourceforge.net/
BuildRequires:	cmake >= 2.8
BuildRequires:	docutils
BuildRequires:	doxygen >= 1.5.0
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	libpng-devel >= 1.0
BuildRequires:	libstdc++-devel
BuildRequires:	make >= 3.81
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	zlib-devel >= 1.0
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
BuildArch:	noarch

%description apidocs
lensfun API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki lensfun.

%package -n python3-lensfun
Summary:	Python 3 interface to lensfun
Summary(pl.UTF-8):	Interfejs Pythoan 3 do lensfun
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-lensfun
Python 3 interface to lensfun.

%description -n python3-lensfun -l pl.UTF-8
Interfejs Pythoan 3 do lensfun.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' apps/lensfun-{add-adapter,update-data}
%{__sed} -i -e '1s,/usr/bin/env sh,%{__sh},' apps/g-lensfun-update-data

# disable, will run manually with our args
%{__sed} -i -e '/INSTALL(.*SETUP_PY.*install/d' apps/CMakeLists.txt

%build
install -d build
cd build
%cmake .. \
	-DBUILD_AUXFUN:BOOL=ON \
	-DBUILD_DOC:BOOL=ON \
	%{cmake_on_off sse BUILD_FOR_SSE} \
	%{cmake_on_off sse2 BUILD_FOR_SSE2} \
	-DBUILD_TESTS:BOOL=OFF \
	-DCMAKE_INSTALL_DOCDIR:PATH=%{_docdir}/%{name}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install/fast \
	DESTDIR=$RPM_BUILD_ROOT

cd build/apps
%py3_install
cd ../..

# packaged as %doc in -apidocs
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README.md docs/{cc-by-sa-3.0,manual-main,mounts}.txt
%attr(755,root,root) %{_libdir}/liblensfun.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblensfun.so.1
%attr(755,root,root) %{_bindir}/g-lensfun-update-data
%attr(755,root,root) %{_bindir}/lensfun-add-adapter
%attr(755,root,root) %{_bindir}/lensfun-update-data
%{_mandir}/man1/g-lensfun-update-data.1*
%{_mandir}/man1/lensfun-add-adapter.1*
%{_mandir}/man1/lensfun-update-data.1*
%{_datadir}/lensfun

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblensfun.so
%{_includedir}/lensfun
%{_pkgconfigdir}/lensfun.pc

%files apidocs
%defattr(644,root,root,755)
%doc build/doc_doxygen/*

%files -n python3-lensfun
%defattr(644,root,root,755)
%{py3_sitescriptdir}/lensfun
%{py3_sitescriptdir}/lensfun-%{version}-py*.egg-info
