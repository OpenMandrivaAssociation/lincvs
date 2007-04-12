%define name	lincvs
%define version 1.4.4
%define release %mkrel 1

Name:		%name
Version:	%version
Release:	%release
Summary:	LinCVS is a graphical interface for the cvs client commandline tool
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
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat >$RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}): command="%{_bindir}/%{name}" needs="X11" \
icon="%{name}.png" section="Applications/Development/Tools" \
title="LinCVS" longtitle="LinCVS is a graphical interface for cvs."
EOF
  
#icon
install -d $RPM_BUILD_ROOT%{_iconsdir}
install -d $RPM_BUILD_ROOT%{_liconsdir}
install -d $RPM_BUILD_ROOT%{_miconsdir}
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
 
%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(755,root,root)
%{_bindir}/%{name}
%dir %{_libdir}/apps/LinCVS
%{_libdir}/apps/LinCVS/*
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/doc/%{name}-%{version}

