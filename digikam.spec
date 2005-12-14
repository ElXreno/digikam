Name:		digikam
Version:	0.8.0
Release:	9%{?dist}
Summary:	A digital camera accessing & photo management application

Group:		Applications/Multimedia
License:	GPL
URL:		http://www.digikam.org/
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:		digikam-0.8.0-gcc41.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gphoto2-devel >= 2.0.0 imlib2-devel libkexif-devel >= 0.2
BuildRequires:	libkipi-devel >= 0.1 sqlite-devel >= 3.0.0 desktop-file-utils
BuildRequires:	libXt-devel libtiff-devel libidn-devel gettext
Requires(post):	desktop-file-utils
Requires(postun): desktop-file-utils

%description
digiKam is an easy to use and powerful digital photo management application,
which makes importing, organizing and manipulating digital photos a "snap".
The photos can be organized in albums which are automatically sorted
chronologically. An easy to use interface is provided to connect to your
digital camera, preview the images and download and/or delete them.

digiKam buildin image editor makes the common photo correction a simple task.
The image editor is extensible via plugins, install the digikamimageplugins
and/or kipi-plugins packages to use them.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the libraries, include files and other resources
needed to develop applications using %{name}.

%prep
%setup -q
%patch0 -p1

%build
unset QTDIR || : ; . /etc/profile.d/qt.sh
export QTLIB=${QTDIR}/lib QTINC=${QTDIR}/include

%configure \
	--disable-rpath \
	--disable-debug
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor fedora --delete-original \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	--add-category X-Fedora \
	--add-category Application \
	--add-category Photograph \
	--add-category Graphics \
	$RPM_BUILD_ROOT%{_datadir}/applnk/Graphics/%{name}.desktop

desktop-file-install --vendor fedora --delete-original \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	--add-category X-Fedora \
	--add-category Application \
	--add-category Photograph \
	--add-category Graphics \
	$RPM_BUILD_ROOT%{_datadir}/applications/kde/showfoto.desktop

%find_lang %{name}

rm -f $RPM_BUILD_ROOT%{_libdir}/libdigikam.la

%post
/sbin/ldconfig
update-desktop-database &> /dev/null ||:

touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
/sbin/ldconfig
update-desktop-database &> /dev/null ||:

touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING HACKING README TODO
%{_bindir}/*
%{_libdir}/libdigikam.so.*
%{_libdir}/kde3/digikamimageplugin_core.la
%{_libdir}/kde3/digikamimageplugin_core.so
%{_libdir}/kde3/kio_digikam*.la
%{_libdir}/kde3/kio_digikam*.so
%{_datadir}/applications/*.desktop
%{_datadir}/apps/digikam/
%{_datadir}/apps/showfoto/
%{_datadir}/icons/hicolor/*
%{_datadir}/services/digikam*
%{_datadir}/servicetypes/digikamimageplugin.desktop

%files devel
%defattr(-, root, root)
%{_includedir}/digikam/
%{_includedir}/digikam_export.h
%{_libdir}/libdigikam.so

%changelog
* Wed Dec 14 2005 Marcin Garski <mgarski@post.pl> 0.8.0-9
- Add libidn-devel to BR

* Wed Dec 14 2005 Marcin Garski <mgarski@post.pl> 0.8.0-8
- Fix compile on GCC 4.1

* Tue Dec 13 2005 Marcin Garski <mgarski@post.pl> 0.8.0-7
- Remove autoreconf

* Tue Dec 13 2005 Marcin Garski <mgarski@post.pl> 0.8.0-6
- Remove patch

* Tue Dec 13 2005 Marcin Garski <mgarski@post.pl> 0.8.0-5
- Last chance to make it right (modular X.Org)

* Tue Dec 13 2005 Marcin Garski <mgarski@post.pl> 0.8.0-4
- Try to build for modular X.Org

* Tue Dec 13 2005 Marcin Garski <mgarski@post.pl> 0.8.0-3
- Add new paths for modular X.Org

* Fri Dec 09 2005 Marcin Garski <mgarski@post.pl> 0.8.0-2
- Work around for modular X.Org paths

* Thu Dec 01 2005 Marcin Garski <mgarski@post.pl> 0.8.0-1
- Add description about digikamimageplugins and kipi-plugins
- Remove 64 bit patch, applied upstream
- Update to version 0.8.0

* Sat Oct 22 2005 Marcin Garski <mgarski@post.pl> 0.7.4-4
- Exclude libdigikam.la (bug #171503)

* Sat Sep 17 2005 Marcin Garski <mgarski@post.pl> 0.7.4-3
- Change confusing warning about Big Endian Platform

* Tue Sep 13 2005 Marcin Garski <mgarski@post.pl> 0.7.4-2
- Spec improvements

* Mon Sep 12 2005 Marcin Garski <mgarski@post.pl> 0.7.4-1
- Updated to version 0.7.4 & clean up for Fedora Extras

* Sat Jun 26 2004 Marcin Garski <mgarski@post.pl> 0.6.2-1.fc2
- Updated to version 0.6.2

* Wed Jun 09 2004 Marcin Garski <mgarski@post.pl> 0.6.2RC-1.fc2
- Initial specfile
