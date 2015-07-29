#define pre rc

%if 0%{?fedora}
%define videoslideshow 1
%endif

Name:    digikam
Version: 4.12.0
Release: 1%{?pre}%{?dist}
Summary: A digital camera accessing & photo management application

License: GPLv2+
URL:     http://www.digikam.org/
Source0: http://download.kde.org/%{?pre:un}stable/digikam/digikam-%{version}%{?pre:-%{pre}}.tar.bz2
%if 0%{?rhel}
# rhel7/ppc64 lacks some dependencies, including libkdcraw, libkexiv2, libkipi
ExcludeArch: ppc64
%endif

# digiKam not listed as a media handler for pictures in Nautilus (#516447)
# TODO: upstream me
Source1: digikam-import.desktop

## upstreamable patches

## upstream patches

BuildRequires: eigen3-devel
BuildRequires: desktop-file-utils
BuildRequires: doxygen
BuildRequires: gettext
%if 0%{?fedora}
BuildRequires: baloo-devel
BuildRequires: kfilemetadata-devel
%endif
# for DLNAExport
BuildRequires: qtsoap-devel
# updated FindKipi.cmake https://bugs.kde.org/show_bug.cgi?id=307213
BuildRequires: kdelibs4-devel >= 4.9.1-4
BuildRequires: kdelibs4-webkit-devel
BuildRequires: kdepimlibs-devel
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(jasper)
BuildRequires: pkgconfig(lcms2)
# libusb required for GPhoto2 support https://bugs.kde.org/268267
# but libgphoto2 switched to libusbx https://bugzilla.redhat.com/997880
BuildRequires: pkgconfig(libusb)
BuildRequires: pkgconfig(libgphoto2_port)
BuildRequires: pkgconfig(libpng) >= 1.2.7
BuildRequires: pkgconfig(libkdcraw) >= 2.2.0
BuildRequires: pkgconfig(libkexiv2) >= 1.0.0
BuildRequires: pkgconfig(libkipi) >= 2.0.0
%if 0%{?fedora}
BuildRequires: pkgconfig(libkface) >= 3.5.0
%define gpssync 1
BuildRequires: pkgconfig(libkgeomap) >= 3.1.0
%endif
BuildRequires: mariadb-server
## DNG converter
BuildRequires: expat-devel
# until when/if libksane-devel grows a depn on sane-backends-devel
BuildRequires: pkgconfig(libksane) 
BuildRequires: sane-backends-devel
## htmlexport plugin
BuildRequires: pkgconfig(libxslt)
## RemoveRedeye
BuildRequires: pkgconfig(opencv) >= 2.4.5
## Shwup
BuildRequires: pkgconfig(qca2)
## debianscreenshorts
BuildRequires: pkgconfig(QJson) 
%if 0%{?videoslideshow}
## VideoSlideShow
# pkgconfig(QtGStreamer-1.0) vs. pkgconfig(QtGStreamer-0.10) is autodetected
BuildRequires: qt-gstreamer-devel
BuildRequires: pkgconfig(ImageMagick)
%endif
# Panorama plugin requires flex and bison
BuildRequires: flex
BuildRequires: bison
%if 0%{?fedora}
BuildRequires: herqq-devel
BuildRequires: pkgconfig(lensfun) >= 0.2.6
BuildRequires: pkgconfig(lqr-1)
%endif
%if 0%{?fedora} || 0%{?rhel} > 6
%define libgpod 1
BuildRequires: pkgconfig(libgpod-1.0)
BuildRequires: pkgconfig(libpgf) >= 6.12.24
%endif

# when lib(-devel) subpkgs were split
Obsoletes: digikam-devel < 2.0.0-2

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kde-runtime%{?_kde4_version: >= %{_kde4_version}}
# http://bugzilla.redhat.com/761184
Requires: kcm_colors
%if 0%{?fedora} > 20
# better default access to mtp-enabled devices
Recommends: kio_mtp
Recommends: kipi-plugins
%endif

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
Requires: %{name} = %{version}-%{release}
%description libs
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kdelibs4-devel
%description devel
This package contains the libraries, include files and other resources
needed to develop applications using %{name}.

%package doc
Summary: Application handbook, documentation, and translations
# for upgrade path
Obsoletes: digikam < 2.5.0-4
Requires:  digikam = %{version}-%{release}
BuildArch: noarch
%description doc
%{summary}.

%package -n libmediawiki
Summary: a MediaWiki C++ interface
%description -n libmediawiki
%{summary}.

%package -n libmediawiki-devel
Summary: Development files for libmediawiki
%description -n libmediawiki-devel
%{summary}.

%package -n libkvkontakte
Summary: Library implementing VKontakte.ru API
%description -n libkvkontakte
KDE C++ library for asynchronous interaction with
vkontakte.ru social network via its open API.

%package -n libkvkontakte-devel
Summary: Development files for libkvkontakte
%description -n libkvkontakte-devel
%{summary}.

%package -n kipi-plugins
Summary: Plugins to use with Kipi
License: GPLv2+ and Adobe
Requires: kipi-plugins-libs%{?_isa} = %{version}-%{release}
## jpeglossless plugin
Requires: ImageMagick
## expoblending
%if 0%{?fedora}
Requires: hugin-base
%endif
%description -n kipi-plugins
This package contains plugins to use with Kipi, the KDE Image Plugin
Interface.  Currently implemented plugins are:
AcquireImages      : acquire images using flat scanner
AdvancedSlideshow  : slide images with 2D and 3D effects using OpenGL
Calendar           : create calendars
DngConverter       : convert Raw Image to Digital NeGative
ExpoBlending       : blend bracketed images
FbExport           : export images to a remote Facebook web service
FlickrExport       : export images to a remote Flickr web service
GalleryExport      : export images to a remote Gallery server
GPSSync            : geolocalize pictures
HTMLExport         : export images collections into a static XHTML page
ImageViewer        : preview images using OpenGL
IpodExport         : export pictures to an Ipod device
JpegLossLess       : rotate/flip images without losing quality
KioExportImport    : export/imports pictures to/from accessible via KIO
MetadataEdit       : edit EXIF, IPTC and XMP metadata
PrintWizard        : print images in various format
RemoveRedEyes      : remove red eyes on image automatically
RawConverter       : convert Raw Image to JPEG/PNG/TIFF
SendImages         : send images by e-mail
SimpleViewerExport : export images to Flash using SimpleViewer
ShwupExport        : export images to a remote Shwup web service
SmugExport         : export images to a remote SmugMug web service
TimeAdjust         : adjust date and time

%package -n kipi-plugins-libs
Summary: Runtime libraries for kipi-plugins
License: GPLv2+ and Adobe
Requires: kipi-plugins = %{version}-%{release}
%{?_kde4_version:Requires: kdelibs4%{?_isa} >= %{_kde4_version}}
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
%description -n kipi-plugins-libs
%{summary}.

%package -n kipi-plugins-doc
Summary: Application handbooks, documentation, and translations
# for upgrade path
Obsoletes: kipi-plugins < 2.5.0-4
Requires:  kipi-plugins = %{version}-%{release}
BuildArch: noarch
%description -n kipi-plugins-doc
%{summary}.


%prep
%setup -q -n %{name}-%{version}%{?pre:-%{pre}}

## HACK to allow building with older opencv (for now), see
# https://bugzilla.redhat.com/show_bug.cgi?id=1119036
sed -i.opencv_245 -e 's|OPENCV_MIN_VERSION "2.4.9"|OPENCV_MIN_VERSION "2.4.5"|' \
  core/CMakeLists.txt \
  extra/kipi-plugins/CMakeLists.txt

# don't use bundled/old FindKipi.cmake in favor of kdelibs' version
# see http:/bugs.kde.org/307213
mv -fv cmake/modules/FindKipi.cmake cmake/modules/FindKipi.cmake.ORIG

# el7's kdelibs doesn't define this entity:
%if 0%{?rhel}
sed -i.docbook_fix -e 's|&Ivo.de.Klerk;||g' doc-translated/*/index.docbook
%endif


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} -DENABLE_LCMS2=ON \
              -DENABLE_KDEPIMLIBSSUPPORT=ON \
              -DDIGIKAMSC_COMPILE_LIBMEDIAWIKI=ON \
              -DDIGIKAMSC_COMPILE_LIBKVKONTAKTE=ON \
              -DENABLE_MYSQLSUPPORT=ON \
              -DENABLE_INTERNALMYSQL=ON \
              ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

desktop-file-install --vendor="" \
  --dir=%{buildroot}%{_datadir}/applications/kde4 \
  %{SOURCE1}

%find_lang digikam --with-kde --without-mo
mv digikam.lang digikam-doc.lang
%find_lang showfoto --with-kde --without-mo
mv showfoto.lang showfoto-doc.lang
cat showfoto-doc.lang >> digikam-doc.lang
%find_lang digikam

%find_lang kipi-plugins --with-kde --without-mo
mv kipi-plugins.lang kipi-plugins-doc.lang
%find_lang kipiplugins
%find_lang kipiplugin_acquireimages
%find_lang kipiplugin_advancedslideshow
%find_lang kipiplugin_batchprocessimages
%find_lang kipiplugin_calendar
%find_lang kipiplugin_dngconverter
%find_lang kipiplugin_expoblending
%find_lang kipiplugin_facebook
%find_lang kipiplugin_flashexport
%find_lang kipiplugin_flickrexport
%find_lang kipiplugin_galleryexport
%if 0%{?gpssync}
%find_lang kipiplugin_gpssync
%endif
%find_lang kipiplugin_htmlexport
%find_lang kipiplugin_imageviewer
%if 0%{?libgpod}
%find_lang kipiplugin_ipodexport
%endif
%find_lang kipiplugin_jpeglossless
%find_lang kipiplugin_kioexportimport
%find_lang kipiplugin_metadataedit
%find_lang kipiplugin_piwigoexport
%find_lang kipiplugin_printimages
%find_lang kipiplugin_rawconverter
%find_lang kipiplugin_removeredeyes
%find_lang kipiplugin_sendimages
%find_lang kipiplugin_shwup
%find_lang kipiplugin_smug
%find_lang kipiplugin_timeadjust
%find_lang kipiplugin_debianscreenshots
%find_lang kipiplugin_dlnaexport
%find_lang kipiplugin_dropbox
%find_lang kipiplugin_googledrive
%find_lang kipiplugin_imageshackexport
%find_lang kipiplugin_imgurexport
%find_lang kipiplugin_jalbumexport
%find_lang kipiplugin_kmlexport
%find_lang kipiplugin_kopete
%find_lang kipiplugin_panorama
%find_lang kipiplugin_photolayouteditor
%find_lang kipiplugin_rajceexport
%find_lang kipiplugin_videoslideshow
%find_lang kipiplugin_vkontakte
%find_lang kipiplugin_wikimedia
%find_lang kipiplugin_yandexfotki
cat kipiplugin_acquireimages.lang kipiplugin_advancedslideshow.lang \
kipiplugin_batchprocessimages.lang kipiplugin_calendar.lang \
kipiplugin_dngconverter.lang kipiplugin_expoblending.lang \
kipiplugin_facebook.lang kipiplugin_flashexport.lang \
kipiplugin_flickrexport.lang kipiplugin_galleryexport.lang \
kipiplugin_htmlexport.lang kipiplugin_imageviewer.lang \
kipiplugin_jpeglossless.lang kipiplugin_kioexportimport.lang \
kipiplugin_metadataedit.lang kipiplugin_photolayouteditor.lang \
kipiplugin_piwigoexport.lang kipiplugin_printimages.lang \
kipiplugin_rawconverter.lang kipiplugin_removeredeyes.lang \
kipiplugin_sendimages.lang kipiplugin_shwup.lang \
kipiplugin_smug.lang kipiplugin_timeadjust.lang \
kipiplugin_debianscreenshots.lang kipiplugin_dlnaexport.lang \
kipiplugin_dropbox.lang kipiplugin_googledrive.lang \
kipiplugin_imageshackexport.lang kipiplugin_imgurexport.lang \
kipiplugin_jalbumexport.lang kipiplugin_kmlexport.lang \
kipiplugin_kopete.lang kipiplugin_panorama.lang \
kipiplugin_rajceexport.lang kipiplugin_videoslideshow.lang \
kipiplugin_wikimedia.lang kipiplugin_yandexfotki.lang \
kipiplugin_vkontakte.lang kipiplugins.lang >> kipi-plugins.lang
%if 0%{?gpssync}
cat kipiplugin_gpssync.lang >> kipi-plugins.lang
%else
rm -fv %{buildroot}%{_datadir}/locale/*/LC_MESSAGES/kipiplugin_gpssync.mo
%endif
%if 0%{?libgpod}
cat kipiplugin_ipodexport.lang >> kipi-plugins.lang
%else
rm -fv %{buildroot}%{_datadir}/locale/*/LC_MESSAGES/kipiplugin_ipodexport.mo
%endif

## unpackaged files
rm -fv %{buildroot}%{_kde4_libdir}/libdigikamcore.so
rm -fv %{buildroot}%{_kde4_libdir}/libdigikamdatabase.so
rm -fv %{buildroot}%{_kde4_libdir}/libkipiplugins.so
rm -fv %{buildroot}%{_kde4_datadir}/locale/*/LC_MESSAGES/libkipi.mo


%check
for i in %{buildroot}%{_kde4_datadir}/applications/kde4/*.desktop ; do
desktop-file-validate $i
done


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
  update-desktop-database -q &> /dev/null
fi

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null

%files -f digikam.lang
%doc core/AUTHORS core/ChangeLog core/COPYING
%doc core/NEWS core/README core/TODO
%{_kde4_bindir}/digikam
%{_kde4_bindir}/digitaglinktree
%{_kde4_bindir}/cleanup_digikamdb
%{_kde4_bindir}/showfoto
%{_kde4_libdir}/kde4/digikam*.so
%{_kde4_libdir}/kde4/kio_digikam*.so
%{_kde4_appsdir}/kconf_update/adjustlevelstool.upd
%{_kde4_appsdir}/digikam/
%{_kde4_appsdir}/showfoto/
%{_kde4_appsdir}/solid/actions/digikam*.desktop
%{_kde4_datadir}/appdata/digiKam-ImagePlugin*xml
%{_kde4_datadir}/appdata/digikam.appdata.xml
%{_kde4_datadir}/appdata/showfoto.appdata.xml
%{_kde4_datadir}/applications/kde4/digikam-import.desktop
%{_kde4_datadir}/applications/kde4/digikam.desktop
%{_kde4_datadir}/applications/kde4/showfoto.desktop
%{_kde4_datadir}/kde4/services/digikam*.desktop
%{_kde4_datadir}/kde4/services/digikam*.protocol
%{_kde4_datadir}/kde4/servicetypes/digikam*.desktop
%{_mandir}/man1/digitaglinktree.1*
%{_mandir}/man1/cleanup_digikamdb.1*
%{_kde4_iconsdir}/hicolor/*/apps/digikam*
%{_kde4_iconsdir}/hicolor/*/apps/showfoto*
%{_kde4_libexecdir}/digikamdatabaseserver

%files doc -f digikam-doc.lang

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kde4_libdir}/libdigikamcore.so.4*
%{_kde4_libdir}/libdigikamdatabase.so.4*

%post -n libmediawiki -p /sbin/ldconfig
%postun -n libmediawiki -p /sbin/ldconfig

%files -n libmediawiki
%doc extra/libmediawiki/AUTHORS extra/libmediawiki/COPYING
%doc extra/libmediawiki/README extra/libmediawiki/COPYING.LIB
%{_kde4_libdir}/libmediawiki.so.1*

%files -n libmediawiki-devel
%{_kde4_libdir}/libmediawiki.so

%post -n libkvkontakte -p /sbin/ldconfig
%postun -n libkvkontakte -p /sbin/ldconfig

%files -n libkvkontakte
%doc extra/libkvkontakte/COPYING extra/libkvkontakte/COPYING.LIB
%{_libdir}/libkvkontakte.so.1
%{_libdir}/libkvkontakte.so.4*

%files -n libkvkontakte-devel
%{_libdir}/libkvkontakte.so
%{_libdir}/cmake/LibKVkontakte/

%post -n kipi-plugins
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null  ||:
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:

%postun -n kipi-plugins
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  touch --no-create %{_kde4_iconsdir}/oxygen  &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor >& /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen >& /dev/null ||:
  update-desktop-database -q &> /dev/null
fi

%posttrans -n kipi-plugins
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor >& /dev/null ||:
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen >& /dev/null ||:
update-desktop-database -q &> /dev/null

%files -n kipi-plugins -f kipi-plugins.lang
%doc extra/kipi-plugins/AUTHORS extra/kipi-plugins/COPYING
%doc extra/kipi-plugins/COPYING-ADOBE extra/kipi-plugins/ChangeLog
%doc extra/kipi-plugins/README extra/kipi-plugins/TODO extra/kipi-plugins/NEWS
%{_kde4_bindir}/dngconverter
%{_kde4_bindir}/expoblending
%{_kde4_bindir}/panoramagui
%{_kde4_bindir}/photolayoutseditor
%{_kde4_bindir}/scangui
%{_kde4_libdir}/kde4/kipiplugin_acquireimages.so
%{_kde4_libdir}/kde4/kipiplugin_advancedslideshow.so
%{_kde4_libdir}/kde4/kipiplugin_batchprocessimages.so
%{_kde4_libdir}/kde4/kipiplugin_calendar.so
%{_kde4_libdir}/kde4/kipiplugin_debianscreenshots.so
%{_kde4_libdir}/kde4/kipiplugin_dngconverter.so
%{_kde4_libdir}/kde4/kipiplugin_dropbox.so
%{_kde4_libdir}/kde4/kipiplugin_facebook.so
%{_kde4_libdir}/kde4/kipiplugin_flickrexport.so
%{_kde4_libdir}/kde4/kipiplugin_flashexport.so
%{_kde4_libdir}/kde4/kipiplugin_galleryexport.so
%{_kde4_libdir}/kde4/kipiplugin_googleservices.so
%if 0%{?gpssync}
%{_kde4_appsdir}/gpssync/
%{_kde4_libdir}/kde4/kipiplugin_gpssync.so
%endif
%{_kde4_libdir}/kde4/kipiplugin_htmlexport.so
%{_kde4_libdir}/kde4/kipiplugin_imageviewer.so
%{_kde4_libdir}/kde4/kipiplugin_imageshackexport.so
%{_kde4_libdir}/kde4/kipiplugin_imgurexport.so
%if 0%{?libgpod}
%{_kde4_libdir}/kde4/kipiplugin_ipodexport.so
%endif
%{_kde4_libdir}/kde4/kipiplugin_jpeglossless.so
%{_kde4_libdir}/kde4/kipiplugin_kioexportimport.so
%{_kde4_libdir}/kde4/kipiplugin_kmlexport.so
%{_kde4_libdir}/kde4/kipiplugin_kopete.so
%{_kde4_libdir}/kde4/kipiplugin_metadataedit.so
%{_kde4_libdir}/kde4/kipiplugin_panorama.so
%{_kde4_libdir}/kde4/kipiplugin_piwigoexport.so
%{_kde4_libdir}/kde4/kipiplugin_printimages.so
%{_kde4_libdir}/kde4/kipiplugin_rajceexport.so
%{_kde4_libdir}/kde4/kipiplugin_rawconverter.so
%{_kde4_libdir}/kde4/kipiplugin_sendimages.so
%{_kde4_libdir}/kde4/kipiplugin_shwup.so
%{_kde4_libdir}/kde4/kipiplugin_smug.so
%{_kde4_libdir}/kde4/kipiplugin_timeadjust.so
%{_kde4_libdir}/kde4/kipiplugin_vkontakte.so
%{_kde4_libdir}/kde4/kipiplugin_yandexfotki.so
%{_kde4_libdir}/kde4/kipiplugin_wikimedia.so
%{_kde4_libdir}/kde4/kipiplugin_dlnaexport.so
%{_kde4_libdir}/kde4/kipiplugin_jalbumexport.so
%if 0%{?videoslideshow}
%{_kde4_libdir}/kde4/kipiplugin_videoslideshow.so
%endif
%{_kde4_appsdir}/kipi/tips
%{_kde4_appsdir}/kipi/*rc
%{_kde4_appsdir}/kipiplugin_flashexport/
%{_kde4_appsdir}/kipiplugin_galleryexport/
%{_kde4_appsdir}/kipiplugin_htmlexport/
%{_kde4_appsdir}/kipiplugin_imageviewer/
%{_kde4_appsdir}/kipiplugin_panorama/
%{_kde4_appsdir}/kipiplugin_piwigoexport/
%{_kde4_appsdir}/kipiplugin_printimages/
%{_kde4_appsdir}/kipiplugin_dlnaexport/
%{_kde4_datadir}/applications/kde4/dngconverter.desktop
%{_kde4_datadir}/applications/kde4/kipiplugins.desktop
%{_kde4_datadir}/applications/kde4/expoblending.desktop
%{_kde4_datadir}/applications/kde4/panoramagui.desktop
%{_kde4_datadir}/applications/kde4/photolayoutseditor.desktop
%{_kde4_datadir}/applications/kde4/scangui.desktop
%{_kde4_datadir}/kde4/services/kipiplugin*.desktop
%{_kde4_iconsdir}/hicolor/*/actions/*
%{_kde4_iconsdir}/hicolor/*/apps/photolayoutseditor*
%{_kde4_iconsdir}/hicolor/*/apps/kipi-*
%{_kde4_iconsdir}/oxygen/*/apps/rawconverter*
%{_kde4_libdir}/kde4/kipiplugin_expoblending.so
%{_kde4_appsdir}/kipiplugin_expoblending/
%{_kde4_libdir}/kde4/kipiplugin_removeredeyes.so
%{_kde4_appsdir}/kipiplugin_removeredeyes/
%{_kde4_libdir}/kde4/kipiplugin_photolayoutseditor.so
%{_kde4_appsdir}/photolayoutseditor/
%{_kde4_datadir}/templates/kipiplugins_photolayoutseditor/
%{_kde4_datadir}/config.kcfg/photolayoutseditor.kcfg
%{_kde4_datadir}/kde4/servicetypes/photolayoutseditor*.desktop

%files -n kipi-plugins-doc -f kipi-plugins-doc.lang

%post -n kipi-plugins-libs -p /sbin/ldconfig
%postun -n kipi-plugins-libs -p /sbin/ldconfig

%files -n kipi-plugins-libs
%{_kde4_libdir}/libkipiplugins.so.4*


%changelog
* Wed Jul 29 2015 Alexey Kurov <nucleo@fedoraproject.org> - 4.12.0-1
- digikam-4.12.0
- old PicasaWeb export removed
- renamed googledrive to googleservices

* Mon Jun 22 2015 Rex Dieter <rdieter@fedoraproject.org> 4.11.0-2
- drop BR: pkgconfig(exiv2), only need libkexiv2-devel these days

* Tue Jun 16 2015 Alexey Kurov <nucleo@fedoraproject.org> - 4.11.0-1
- digikam-4.11.0

* Sat May 23 2015 Rex Dieter <rdieter@fedoraproject.org> 4.10.0-5
- hugin-base not available in epel-7

* Mon May 18 2015 Rex Dieter <rdieter@fedoraproject.org> 4.10.0-4
- merge epel-7 mods (#1194901)

* Sat May 16 2015 Rex Dieter <rdieter@fedoraproject.org> 4.10.0-3
- export menu wont appear (#1222225)

* Thu May 14 2015 Nils Philippsen <nils@redhat.com> - 4.10.0-2
- rebuild for lensfun-0.3.1

* Tue May 12 2015 Alexey Kurov <nucleo@fedoraproject.org> - 4.10.0-1
- digikam-4.10.0
- added more kipiplugin translations

* Mon Apr 20 2015 Alexey Kurov <nucleo@fedoraproject.org> - 4.9.0-2
- build against system libkface and libkgeomap

* Tue Apr  7 2015 Alexey Kurov <nucleo@fedoraproject.org> - 4.9.0-1
- digikam-4.9.0
- removed libkgeomap translations

* Mon Feb 23 2015 Alexey Kurov <nucleo@fedoraproject.org> - 4.8.0-1
- digikam-4.8.0

* Tue Feb  3 2015 Alexey Kurov <nucleo@fedoraproject.org> - 4.7.0-2
- rebuild

* Tue Feb  3 2015 Alexey Kurov <nucleo@fedoraproject.org> - 4.7.0-1
- digikam-4.7.0

* Wed Jan 21 2015 Peter Robinson <pbrobinson@fedoraproject.org> 4.6.0-3
- Rebuild (libgpohoto2)

* Tue Jan 20 2015 Rex Dieter <rdieter@fedoraproject.org> 4.6.0-2
- bump release

* Tue Jan 20 2015 Rex Dieter <rdieter@fedoraproject.org> 4.6.0-1.1
- rebuild (marble, f20/f21)

* Thu Dec 18 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.6.0-1
- digikam-4.6.0

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-3
- rebuild (marble)
- drop libjpeg-turbo workarounds (not needed anymore)

* Mon Nov 17 2014 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-2
- fix/workaround FTBFS against newer libjpeg-turbo (kde#340944)

* Fri Nov 14 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.5.0-1
- digikam-4.5.0

* Thu Oct  9 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.4.0-1
- digikam-4.4.0

* Sat Sep 20 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.3.0-2
- backport job crash fix (kde bugs 325580, 339210)

* Tue Sep 16 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.3.0-1
- digikam-4.3.0
- add BR: baloo-devel kfilemetadata-devel

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-5
- core/CMakeLists.txt too (#1119036)

* Wed Aug 13 2014 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-4
- hack to allow build with older opencv (#1119036)

* Thu Aug 07 2014 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-3
- rebuild (marble)

* Wed Aug  6 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.2.0-2
- enable kdepimlibs support disabled by default in 4.2.0 (kde#338055)

* Mon Aug  4 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.2.0-1
- digikam-4.2.0

* Sun Aug 03 2014 Rex Dieter <rdieter@fedoraproject.org> 4.1.0-4
- make kio_mtp fedora only

* Wed Jul 23 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.1.0-3
- apply upstream patch to handle QtGstreamer API 1.0 in VideoSlideShow tool;
  whether to build against QtGStreamer 0.10 or 1.x is autodetected (#1092659)

* Mon Jul 14 2014 Rex Dieter <rdieter@fedoraproject.org> 4.1.0-2
- rebuild (marble)

* Sun Jun 29 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.1.0-1
- digikam-4.1.0
- OpenCV >= 2.4.9 required for libkface

* Thu Jun 19 2014 Rex Dieter <rdieter@fedoraproject.org> 4.0.0-3
- BR: kdelibs4-webkit-devel

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.0.0-1
- digikam-4.0.0

* Mon Apr 28 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.0.0-0.8.rc
- digikam-4.0.0-rc

* Sat Apr 26 2014 Rex Dieter <rdieter@fedoraproject.org> 4.0.0-0.7.beta4
- rebuild (opencv)

* Mon Mar 31 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.0.0-0.6.beta4
- rebuild for ImageMagick-6.8.8.10
- drop BR: nepomuk-core-devel (Nepomuk disabled by default kde#332665)

* Thu Mar 27 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.0.0-0.5.beta4
- digikam-4.0.0-beta4
- add BR: nepomuk-core-devel

* Thu Mar 20 2014 Rex Dieter <rdieter@fedoraproject.org> 4.0.0-0.4.
- rebuild (kde-4.13)

* Tue Feb 25 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.0.0-0.3.beta3
- digikam-4.0.0-beta3

* Tue Jan 14 2014 Alexey Kurov <nucleo@fedoraproject.org> - 4.0.0-0.2.beta2
- digikam-4.0.0-beta2

* Mon Dec  9 2013 Alexey Kurov <nucleo@fedoraproject.org> - 4.0.0-0.1.beta1
- digikam-4.0.0-beta1

* Tue Dec 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 3.5.0-4
- rebuild (exiv2)

* Sat Nov 16 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.5.0-3
- rebuilt for libkdcraw-4.11.90

* Thu Oct 10 2013 Rex Dieter <rdieter@fedoraproject.org> 3.5.0-2
- include (upstreamable) patch to omit libPropertyBrowser from packaging (kde#319664)

* Wed Oct  9 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.5.0-1
- digikam-3.5.0

* Fri Sep  6 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.4.0-1
- digikam-3.4.0
- BuildRequires: pkgconfig(libusb)

* Thu Sep 05 2013 Rex Dieter <rdieter@fedoraproject.org> 3.3.0-2
- rebuild (kde-4.11.x)

* Mon Aug  5 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.3.0-1
- digikam-3.3.0

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 3.3.0-0.6.beta3
- Perl 5.18 rebuild

* Mon Jul  8 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.3.0-0.5.beta3
- digikam-3.3.0-beta3

* Fri Jun 28 2013 Rex Dieter <rdieter@fedoraproject.org> 3.3.0-0.4.beta2
- rebuild (marble)

* Thu Jun 27 2013 Rex Dieter <rdieter@fedoraproject.org> 3.3.0-0.3.beta2
- rebuild (libkipi)

* Sat Jun 22 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.3.0-0.2.beta2
- digikam-3.3.0-beta2

* Tue Jun  4 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.3.0-0.1.beta1
- digikam-3.3.0-beta1

* Fri May 31 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.2.0-5
- more fixes for bars hiding in fullscreen mode kde#319876

* Thu May 30 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.2.0-4
- fix thumbbar visibility after fullscreen mode kde#319876

* Wed May 29 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.2.0-3
- fix sidebar in fullscreen mode kde#319876

* Wed May 29 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.2.0-2
- fix fullscreen settings loading kde#320016

* Tue May 14 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.2.0-1
- digikam-3.2.0

* Wed May  1 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.2.0-0.2.beta2
- digikam-3.2.0-beta2

* Mon Apr  8 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.2.0-0.1.beta1
- digikam-3.2.0-beta1
- BR: eigen3-devel instead of atlas-devel, drop clapack patch

* Sun Mar 17 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.1.0-2
- rebuild for ImageMagick-6.8.3.9

* Tue Mar 12 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.1.0-1
- digikam-3.1.0
- drop BR: pkgconfig(sqlite3) mysql-devel

* Wed Mar 06 2013 Rex Dieter <rdieter@fedoraproject.org> 3.0.0-2
- rebuild (marble)

* Fri Feb  8 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.0.0-1
- digikam-3.0.0
- BR: flex bison for Panorama plugin

* Mon Jan 28 2013 Rex Dieter <rdieter@fedoraproject.org> 3.0.0-0.16.rc
- Requires: kio_mtp

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 3.0.0-0.15.rc
- rebuild due to "jpeg8-ABI" feature drop

* Thu Jan 3 2013 Lukáš Tinkl <ltinkl@redhat.com> -  - 3.0.0-0.14.rc
- Resolves #891515, build marble deps on Fedora only

* Sat Dec 29 2012 Alexey Kurov <nucleo@fedoraproject.org> - 3.0.0-0.13.rc
- digikam-3.0.0-rc
- disable local kdegraphics build enabled in rc by default

* Thu Dec 13 2012 Rex Dieter <rdieter@fedoraproject.org> 3.0.0-0.12.beta3
- cleanup, remove old conditionals, Conflicts

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> 3.0.0-0.11.beta3
- rebuild (marble)

* Tue Nov 27 2012 Rex Dieter <rdieter@fedoraproject.org> 3.0.0-0.10.beta3
- rebuild (qjson)

* Fri Nov 23 2012 Alexey Kurov <nucleo@fedoraproject.org> - 3.0.0-0.9.beta3
- rebuild for qjson-0.8.0

* Sun Nov 11 2012 Alexey Kurov <nucleo@fedoraproject.org> - 3.0.0-0.8.beta3
- digikam-3.0.0-beta3

* Mon Nov 05 2012 Rex Dieter <rdieter@fedoraproject.org> 3.0.0-0.6.beta2
- rebuild (opencv)

* Wed Oct 24 2012 Alexey Kurov <nucleo@fedoraproject.org> - 3.0.0-0.5.beta2
- rebuild for libjpeg8

* Sat Oct 13 2012 Alexey Kurov <nucleo@fedoraproject.org> - 3.0.0-0.4.beta2
- digikam-3.0.0-beta2

* Wed Sep 26 2012 Rex Dieter <rdieter@fedoraproject.org> 3.0.0-0.3.beta1a
- rebuild for updated FindKipi.cmake in kdelibs (kde#307213)

* Sat Sep 22 2012 Alexey Kurov <nucleo@fedoraproject.org> - 3.0.0-0.2.beta1a
- rebuild for updated FindKipi.cmake in kdelibs (kde#307213)

* Fri Sep 21 2012 Alexey Kurov <nucleo@fedoraproject.org> - 3.0.0-0.1.beta1a
- digikam-3.0.0-beta1a

* Sun Sep  2 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.9.0-1
- digikam-2.9.0

* Fri Aug 17 2012 Rex Dieter <rdieter@fedoraproject.org> 2.8.0-3
- rev libgphoto2-2.5 patch (kde#303427)

* Fri Aug 10 2012 Rex Dieter <rdieter@fedoraproject.org> 2.8.0-2
- rebuild (libimobiledevice)

* Mon Aug  6 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.8.0-1
- digikam-2.8.0

* Tue Jul 24 2012 Rex Dieter <rdieter@fedoraproject.org> 2.7.0-5
- digikam FTBFS against libgphoto2-2.5 (#841615)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.7.0-3
- rebuild for libgphoto2-2.5.0

* Tue Jul 10 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.7.0-2
- rebuild for opencv-2.4.2

* Sun Jul  8 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.7.0-1
- digikam-2.7.0

* Thu Jun 28 2012 Rex Dieter <rdieter@fedoraproject.org> 2.6.0-3
- fix build for newer lensfun-0.2.6+

* Tue Jun 26 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.6.0-2
- rebuild for libpgf-6.12.24

* Tue Jun  5 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.6.0-1
- digikam-2.6.0

* Tue May 29 2012 Rex Dieter <rdieter@fedoraproject.org> 2.6.0-0.10.rc
- rebuild (kde-4.9beta)

* Wed May 16 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.6.0-0.9.rc
- switch to lcms2, fix dkCmsTakeProfileID allocation size (kde#299886)

* Tue May 15 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.6.0-0.8.rc
- switch back to lcms1 for now (kde#299886)

* Wed May  9 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.6.0-0.7.rc
- digikam-software-compilation-2.6.0-rc

* Tue May 08 2012 Rex Dieter <rdieter@fedoraproject.org> 2.6.0-0.6.beta3
- rebuild (libtiff)

* Wed May 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 2.6.0-0.5.beta3
- rebuild (exiv2)

* Thu Apr 12 2012 Rex Dieter <rdieter@fedoraproject.org> 2.6.0-0.4.beta3.1
- rebuild (usbmuxd)

* Mon Apr  2 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.6.0-0.4.beta3
- digikam-2.6.0-beta3

* Tue Mar  6 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.6.0-0.3.beta2
- digikam-2.6.0-beta2

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-0.2.beta1
- Rebuilt for c++ ABI breakage

* Tue Feb  7 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.6.0-0.1.beta1
- digikam-2.6.0-beta1
- drop upstreamed patches gcc-4.7.0, dngconverter_hicolor_icons, libkipi, boost

* Thu Feb 02 2012 Rex Dieter <rdieter@fedoraproject.org> 2.5.0-5
- Requires: kcm_colors (kde48+)

* Thu Feb 02 2012 Rex Dieter <rdieter@fedoraproject.org> 2.5.0-4
- -doc, kipi-plugins-doc subpkgs for largish HTML handbooks
- upstreamed dng patch

* Sat Jan  7 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.5.0-3
- update boost patch

* Thu Jan  5 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.5.0-2
- fix build with gcc-4.7.0 (kde#290642) and boost-1.48 (kde#287772)

* Tue Jan  3 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.5.0-1
- digikam-2.5.0

* Fri Dec 09 2011 Rex Dieter <rdieter@fedoraproject.org> 2.4.1-2
- make dngconverter app icons to hicolor so usable outside of kde (#682055)

* Mon Dec  5 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.4.1-1
- digikam-2.4.1
- drop icons and tooltips patches (in upstream now)

* Mon Nov 21 2011 Rex Dieter <rdieter@fedoraproject.org> 2.3.0-4
- Unreadable text on tooltips in KDE 4.7 (kde#283572)

* Tue Nov 15 2011 Rex Dieter <rdieter@fedoraproject.org> 2.3.0-3
- BR: libjpeg-devel

* Tue Nov  8 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.3.0-2
- fix collision of digiKam icons with Oxygen

* Mon Nov  7 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.3.0-1
- digikam-2.3.0
- drop libpgf-api patch

* Sat Oct 29 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.2.0-2
- rebuild for libpgf-6.11.42
- bacport fix for changed libpgf API

* Tue Oct  4 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.2.0-1
- digikam-2.2.0
- drop libkvkontakte-libdir patch
- added photolayoutseditor in kipi-plugins

* Wed Sep 28 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1.1-5
- include marble epoch in deps

* Mon Sep 26 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.1.1-4
- BR: pkgconfig(libpgf)

* Mon Sep 26 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1.1-3
- pkgconfig-style deps

* Fri Sep 23 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.1.1-2
- BuildRequires: atlas-devel (for clapack, instead of the bundled version)
- fix FindCLAPACK.cmake to search %%{_libdir}/atlas
- patch matrix.cpp for the ATLAS clapack API

* Wed Sep 14 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.1.1-1
- digikam-2.1.1

* Fri Sep  9 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.1.0-1
- digikam-2.1.0
- drop qt_rasterengine patch
- add libkvkontakte subpkg

* Sun Aug 21 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-4
- rebuild (opencv)

* Thu Aug 18 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-3
- digikam crashes with "-graphicssystem raster" (#726971)

* Tue Aug 02 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-2
- new libkface, libkgeomap, libmediawiki subpkgs (#727570)
- remove rpm cruft (%%clean, %%defattr, Group:, BuildRoot:)

* Fri Jul 29 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.0.0-1
- digikam-2.0.0
- drop s390 patch included upstream
- bundled code not used by default (DIGIKAMSC_USE_PRIVATE_KDEGRAPHICS not defined)

* Thu Jul 07 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-0.2.rc
- use pkgconfig()-style deps for libkdcraw, libkexiv2, libkipi, libksane
- -libs: drop (versioned) dep on kdegraphics-libs

* Thu Jun 30 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.0.0-0.1.rc
- digikam-2.0.0-rc
- merge with kipi-plugins.spec

* Wed Jun 15 2011 Rex Dieter <rdieter@fedoraproject.org> 1.9.0-2
- rebuild (marble)

* Thu Mar 17 2011 Rex Dieter <rdieter@fedoraproject.org> 1.9.0-1
- 1.9.0

* Thu Mar 03 2011 Rex Dieter <rdieter@fedoraproject.org> 1.8.0-3
- use safer check for libjpeg version, using cmake_try_compile (kde#265431)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Rex Dieter <rdieter@fedoraproject.org> 1.8.0-1
- 1.8.0

* Wed Dec 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.7.0-1
- digikam-1.7.0

* Tue Nov 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.6.0-1
- digikam-1.6.0 (#628156)

* Tue Nov 02 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.5.0-1.1
- -libs: add minimal kdegraphics-libs dep (#648741)

* Mon Oct 11 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.5.0-1
- digikam-1.5.0

* Wed Aug 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-1
- digikam-1.4.0

* Tue Jun 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.3.0-1
- digikam-1.3.0

* Tue Mar 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.2.0-2
- crash on startup in RatingWidget (kde#232628)

* Mon Mar 29 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.2.0-1
- digikam-1.2.0

* Mon Mar 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-3
- -libs: drop extraneous deps
- -devel: Req: kdelibs4-devel

* Wed Feb 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-2
- touch up marble-related deps

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

* Sun Nov 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.0-0.8.beta6
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

* Tue Nov 20 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-0.2.beta3
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
