
Name:	 digikam
Version: 1.1.0
Release: 1%{?dist}
Summary: A digital camera accessing & photo management application

Group:	 Applications/Multimedia
License: GPLv2+
URL:	 http://www.digikam.org/
Source0: http://downloads.sourceforge.net/digikam/digikam-%{version}%{?pre:-%{pre}}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# digiKam not listed as a media handler for pictures in Nautilus (#516447)
Source1: digikam-import.desktop

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: glib2-devel
BuildRequires: gphoto2-devel
BuildRequires: libkdcraw-devel >= 0.4.0-2
BuildRequires: libkexiv2-devel >= 0.5.0
BuildRequires: libkipi-devel >= 0.3.0
BuildRequires: liblqr-1-devel
BuildRequires: jasper-devel

# marble integration, http://bugzilla.redhat.com/470578 
%define marble_version 4.3.0
BuildRequires: kdeedu-devel >= %{marble_version} 

BuildRequires: kdelibs4-devel

# trash protocol support needed
# FIXME: should probably be handled lower in the stack
Requires: kdebase-runtime%{?_kde4_version: >= %{_kde4_version}}

BuildRequires: kdepimlibs-devel
BuildRequires: lcms-devel
BuildRequires: lensfun-devel
BuildRequires: libtiff-devel
BuildRequires: libpng-devel >= 1.2.7
BuildRequires: soprano-devel
BuildRequires: sqlite-devel

Obsoletes: digikamimageplugins < 0.9.1-2

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
digiKam is an easy to use and powerful digital photo management application,
which makes importing, organizing and manipulating digital photos a "snap".
An easy to use interface is provided to connect to your digital camera,
preview the images and download and/or delete them.

digiKam built-in image editor makes the common photo correction a simple task.
The image editor is extensible via plugins, can also make use of the KIPI image
handling plugins to extend its capabilities even further for photo
manipulations, import and export, etc. Install the kipi-plugins packages
to use them.

%package libs
Summary: Runtime libraries for %{name}
Group:   System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%{?_kde4_version:Requires: kdelibs4%{?_isa} >= %{_kde4_version}}
Requires: kdeedu-marble-libs%{?_isa} >= %{marble_version}
%description libs
%{summary}.

%package devel
Summary: Development files for %{name}
Group:	 Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
This package contains the libraries, include files and other resources
needed to develop applications using %{name}.


%prep
%setup -q -n %{name}-%{version}%{?pre:-%{pre}}


%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

desktop-file-install --vendor="" \
  --dir=%{buildroot}%{_datadir}/applications/kde4 \
  %{SOURCE1}

%find_lang digikam --with-kde


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/kde4/digikam.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/kde4/showfoto.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  update-desktop-database -q &> /dev/null
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
update-desktop-database -q &> /dev/null
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%clean
rm -rf %{buildroot}


%files -f digikam.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING HACKING NEWS README TODO
%{_kde4_bindir}/*
%{_kde4_libdir}/kde4/*.so
%{_kde4_appsdir}/digikam/
%{_kde4_appsdir}/showfoto/
%{_kde4_appsdir}/solid/actions/*.desktop
%{_kde4_datadir}/applications/kde4/*.desktop
%{_kde4_datadir}/kde4/services/*.desktop
%{_kde4_datadir}/kde4/services/*.protocol
%{_kde4_datadir}/kde4/servicetypes/*.desktop
%{_mandir}/man1/*
%{_kde4_iconsdir}/hicolor/*/*/*

%files libs
%defattr(-,root,root,-)
%{_kde4_libdir}/libdigikamcore.so.1*
%{_kde4_libdir}/libdigikamdatabase.so.1*
%{_kde4_libdir}/kde4/plugins/marble/ExternalDraw.so

%files devel
%defattr(-,root,root,-)
%{_kde4_includedir}/digikam/
%{_kde4_includedir}/digikam_export.h
%{_kde4_libdir}/lib*.so


%changelog
* Mon Feb 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-1
- digikam-1.1.0

* Thu Jan 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-2
- use %%{_kde4_version}

* Mon Dec 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-1
- digikam-1.0.0

* Mon Nov 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.11.rc
- digikam-1.0.0-rc

* Wed Nov 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.10.beta6
- rebuild (kdegraphics)

* Sat Nov 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.9.beta6
- digiKam not listed as a media handler for pictures in Nautilus (#516447)

* Mon Nov 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.8.beta6
- digikam-1.0.0-beta6

* Tue Oct 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.7.beta5
- digikam-1.0.0-beta5
- tweak marble deps (again)

* Tue Sep 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.6.beta4
- fix marble dep(s)

* Mon Aug 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.5.beta4
- digikam-1.0.0-beta4
- BR: liblqr-1-devel

* Wed Aug 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.4.beta3
- drop xdg-utils references 
- tighten -libs related deps via %%{?_isa}

* Fri Jul 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.3.beta3
- digikam-1.0.0-beta3

* Mon Jul 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.2.beta2
- digikam-1.0.0-beta2

* Fri Jun 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.1.beta1
- digikam-1.0.0-beta1

* Tue Mar 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-1
- digikam-0.10.0 (final)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-0.18.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.17.rc2
- digikam-0.10.0-rc2

* Mon Feb 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.16.rc1
- Req: kdebase-runtime

* Wed Feb 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.15.rc1
- BR: kdeedu-devel >= 4.2.0, Req: kdeedu-marble >= 4.2.0
- add min Req: kdelibs4 dep too 

* Thu Jan 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10-0-0.14.rc1
- digikam-0.10.0-rc1

* Mon Jan 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10-0.13.beta8
- re-enable marble integration, kde42+ (bug #470578)

* Mon Jan 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.12.beta8
- digikam-0.10.0-beta8

* Mon Dec 22 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.11.beta7
- BR: libkipi-devel >= 0.3.0

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.9.beta7
- digikam-0.10.0-beta7

* Mon Dec 01 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.8.beta6
- omit kde42 (icon) conflicts

* Tue Nov 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.7.beta6
- digikam-0.10.0-beta6
- lensfun support

* Mon Oct 27 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.6.beta5
- digikam-0.10.0-beta5

* Mon Oct 06 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.10.0-0.5.beta4
- update to 0.10.0 beta 4
- build against latest kdegraphics

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.4.beta3
- digikam-0.10.0-beta3

* Mon Aug 04 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.3.beta2
- disable marble integration

* Sat Aug 02 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.2.beta2
- omit conflicts with oxygen-icon-theme

* Thu Jul 31 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-0.1.beta2
- digikam-0.10.0-beta2

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.9.4-2
- --without-included-sqlite3, BR: sqlite-devel

* Thu Jul 17 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.9.4-1
- digikam-0.9.4

* Mon Jul 07 2008 Marcin Garski <mgarski[AT]post.pl> 0.9.3-5
- Don't lose some photos during import (#448235)

* Fri Mar 14 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.9.3-3
- respin (for libkdcraw)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.3-2
- Autorebuild for GCC 4.3

* Sat Dec 22 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.3-1
- Update to 0.9.3
- BR: libkexiv2-devel >= 0.1.6 libkdcraw-devel >= 0.1.2

* Sat Dec 08 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-0.5.rc1
- digikam-0.9.3-rc1
- BR: kdelibs3-devel

* Thu Nov 20 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-0.2.beta3
- digikam-0.9.3-beta3

* Tue Nov 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-0.1.beta2
- digikam-0.9.3-beta2

* Tue Sep 18 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.2-5
- Rebuild

* Wed Aug 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-4
- License: GPLv2+
- lcms patch (kde bug #148930)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.9.2-3
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.2-2
- Create symlinks in pixmaps directory (#242978)

* Tue Jun 19 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.2-1
- Update to version 0.9.2-final
- Remove digikam-0.9.2-beta3-fix-exiv2-dep.patch, merged upstream

* Wed Jun 06 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.2-0.3.beta3
- Fix .desktop category

* Wed Jun 06 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.2-0.2.beta3
- Fix broken compilation caused by Exiv2 dependency

* Tue Jun 05 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.2-0.1.beta3
- Update to version 0.9.2-beta3 (merge with digikamimageplugins)
- Update description

* Mon May 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.1-3
- respin against libkexiv2-0.1.5
- preserve upstream .desktop vendor (f7 branch at least)

* Mon Apr 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.1-2
- exiv2-0.14 patch
- cleanup/simplify BR's,Requires,d-f-i usage

* Fri Mar 09 2007 Marcin Garski <mgarski[AT]post.pl> 0.9.1-1
- Update to version 0.9.1
- Update BuildRequires

* Mon Dec 18 2006 Marcin Garski <mgarski[AT]post.pl> 0.9.0-1
- Update to version 0.9.0

* Tue Nov 28 2006 Marcin Garski <mgarski[AT]post.pl> 0.9.0-0.2.rc1
- Rebuild

* Tue Nov 28 2006 Marcin Garski <mgarski[AT]post.pl> 0.9.0-0.1.rc1
- Update to version 0.9.0-rc1

* Fri Sep 01 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.2-3
- Rebuild for Fedora Core 6

* Wed Aug 16 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.2-2
- Release bump (#201756)

* Tue Aug 01 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.2-1
- Update to version 0.8.2 (#200932)

* Tue Feb 14 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.1-3
- Rebuild

* Wed Feb 08 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.1-2
- Exclude x-raw.desktop (bug #179754)
- Don't own icons directory

* Mon Jan 23 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.1-1
- Add --enable-final
- Remove GCC 4.1 patch, applied upstream
- Update to version 0.8.1

* Mon Jan 23 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.0-16
- Add some stuff to BuildRequires (finally fix bug #178031)

* Tue Jan 17 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.0-15
- Remove redundant BuildRequires (bug #178031)

* Mon Jan 16 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.0-14
- Remove --disable-dependency-tracking

* Mon Jan 16 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.0-13
- Remove --enable-final (caused compilation errors)

* Sun Jan 15 2006 Marcin Garski <mgarski[AT]post.pl> 0.8.0-12
- Change "/etc/profile.d/qt.sh" to "%%{_sysconfdir}/profile.d/qt.sh"
- Add --disable-dependency-tracking & --enable-final

* Wed Dec 14 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-11
- Add libart_lgpl-devel and gamin-devel to BR

* Wed Dec 14 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-10
- Add libacl-devel to BR

* Wed Dec 14 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-9
- Add libidn-devel to BR

* Wed Dec 14 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-8
- Fix compile on GCC 4.1

* Tue Dec 13 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-7
- Remove autoreconf

* Tue Dec 13 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-6
- Remove patch

* Tue Dec 13 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-5
- Last chance to make it right (modular X.Org)

* Tue Dec 13 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-4
- Try to build for modular X.Org

* Tue Dec 13 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-3
- Add new paths for modular X.Org

* Fri Dec 09 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-2
- Work around for modular X.Org paths

* Thu Dec 01 2005 Marcin Garski <mgarski[AT]post.pl> 0.8.0-1
- Add description about digikamimageplugins and kipi-plugins
- Remove 64 bit patch, applied upstream
- Update to version 0.8.0

* Sat Oct 22 2005 Marcin Garski <mgarski[AT]post.pl> 0.7.4-4
- Exclude libdigikam.la (bug #171503)

* Sat Sep 17 2005 Marcin Garski <mgarski[AT]post.pl> 0.7.4-3
- Change confusing warning about Big Endian Platform

* Tue Sep 13 2005 Marcin Garski <mgarski[AT]post.pl> 0.7.4-2
- Spec improvements

* Mon Sep 12 2005 Marcin Garski <mgarski[AT]post.pl> 0.7.4-1
- Updated to version 0.7.4 & clean up for Fedora Extras

* Sat Jun 26 2004 Marcin Garski <mgarski[AT]post.pl> 0.6.2-1.fc2
- Updated to version 0.6.2

* Wed Jun 09 2004 Marcin Garski <mgarski[AT]post.pl> 0.6.2RC-1.fc2
- Initial specfile
