#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.112
%define		qtver		5.15.2
%define		kfname		kcmutils

Summary:	Utilities for KDE System Settings modules
Name:		kf5-%{kfname}
Version:	5.112.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	bdb42bbf2f1eab7971344d83e3d72768
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-devel
BuildRequires:	kf5-attica-devel >= %{version}
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-kauth-devel >= %{version}
BuildRequires:	kf5-kcodecs-devel >= %{version}
BuildRequires:	kf5-kcompletion-devel >= %{version}
BuildRequires:	kf5-kconfig-devel >= %{version}
BuildRequires:	kf5-kconfigwidgets-devel >= %{version}
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	kf5-kdbusaddons-devel >= %{version}
BuildRequires:	kf5-kdeclarative-devel >= %{version}
BuildRequires:	kf5-kglobalaccel-devel >= %{version}
BuildRequires:	kf5-kguiaddons-devel >= %{version}
BuildRequires:	kf5-ki18n-devel >= %{version}
BuildRequires:	kf5-kiconthemes-devel >= %{version}
BuildRequires:	kf5-kitemviews-devel >= %{version}
BuildRequires:	kf5-kservice-devel >= %{version}
BuildRequires:	kf5-ktextwidgets-devel >= %{version}
BuildRequires:	kf5-kwidgetsaddons-devel >= %{version}
BuildRequires:	kf5-kwindowsystem-devel >= %{version}
BuildRequires:	kf5-kxmlgui-devel >= %{version}
BuildRequires:	kf5-sonnet-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KCMUtils provides various classes to work with KCModules. KCModules
can be created with the KConfigWidgets framework.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	kf5-kconfigwidgets-devel >= %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF5KCMUtils.so.5
%attr(755,root,root) %{_libdir}/libKF5KCMUtils.so.*.*
%ghost %{_libdir}/libKF5KCMUtilsCore.so.5
%attr(755,root,root) %{_libdir}/libKF5KCMUtilsCore.so.*.*
%{_datadir}/kservicetypes5/kcmodule.desktop
%{_datadir}/kservicetypes5/kcmoduleinit.desktop
%{_datadir}/qlogging-categories5/kcmutils.categories
%dir %{_libdir}/qt5/qml/org/kde/kcmutils
%dir %{_libdir}/qt5/qml/org/kde/kcmutils/components
%{_libdir}/qt5/qml/org/kde/kcmutils/components/KPluginDelegate.qml
%{_libdir}/qt5/qml/org/kde/kcmutils/components/KPluginSelector.qml
%dir %{_libdir}/qt5/qml/org/kde/kcmutils/components/private
%{_libdir}/qt5/qml/org/kde/kcmutils/components/private/AboutPlugin.qml
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/kcmutils/libkcmutilsqmlplugin.so
%{_libdir}/qt5/qml/org/kde/kcmutils/qmldir
%attr(755,root,root) %{_prefix}/libexec/kf5/kcmdesktopfilegenerator

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KCMUtils
%{_libdir}/cmake/KF5KCMUtils
%{_libdir}/libKF5KCMUtils.so
%{qt5dir}/mkspecs/modules/qt_KCMUtils.pri
%{_includedir}/KF5/KCMUtilsCore
%{_libdir}/libKF5KCMUtilsCore.so

