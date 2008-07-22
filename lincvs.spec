%define name	lincvs
%define version 1.4.4
%define release %mkrel 3

Name:		%name
Version:	%version
Release:	%release
Summary:	Graphical interface for the cvs client commandline tool
License:	GPL
Group:		Development/Other
URL:		http://www.lincvs.org/
Source0:	%name-%version-0-generic-src.tar.bz2
Source1:	%{name}_16.png
Source2:	%{name}_32.png
Source3:	%{name}_48.png
BuildRoot: 	%{_tmppath}/%{name}-buildroot
BuildRequires:	qt3-devel
Requires:	cvs

%description
LinCVS is a graphical interface for the cvs client commandline tool.
In contrast to other programs this one is really easy to use ;-) .

%prep
%setup -q
chmod a+rw ts/*

%build
# Generate Makefile
%{_prefix}/lib/qt3/bin/qmake -o Makefile lincvs.pro QTDIR=%{_prefix}/lib/qt3
%make QTDIR=%{_prefix}/lib/qt3

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std QTDIR=%{_prefix}/lib/qt3 INSTALL_ROOT=$RPM_BUILD_ROOT%{_libdir}/apps/

install -d $RPM_BUILD_ROOT%{_bindir}

# Generate a wrapper script
echo \#\!/bin/bash > $RPM_BUILD_ROOT%{_bindir}/%{name}
echo exec\ \"%{_libdir}/apps/LinCVS/lincvs.bin\" >> $RPM_BUILD_ROOT%{_bindir}/%{name}
chmod 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

# Fix permissions
find $RPM_BUILD_ROOT%{_libdir}/apps/LinCVS/{Help,Messages}/ -type f -depth -exec chmod 644 {} \;
find $RPM_BUILD_ROOT%{_libdir}/apps/LinCVS/Tools/ -type f -depth -exec chmod 755 {} \;

# Make symlink for docs
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc
cd $RPM_BUILD_ROOT%{_datadir}/doc
ln -s ../../..%{_libdir}/apps/LinCVS/Help  %{name}-%{version}


# Menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/%{name}
Icon=%{name}
Categories=X-MandrivaLinux-MoreApplications-Development-Tools;Development;
Name=LinCVS
Comment=LinCVS is a graphical interface for cvs.
EOF
  
#icon
install -d $RPM_BUILD_ROOT%{_iconsdir}
install -d $RPM_BUILD_ROOT%{_liconsdir}
install -d $RPM_BUILD_ROOT%{_miconsdir}
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
 
%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(755,root,root)
%{_bindir}/%{name}
%dir %{_libdir}/apps/LinCVS
%{_libdir}/apps/LinCVS/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/doc/%{name}-%{version}


