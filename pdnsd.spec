# $Id: pdnsd.spec.in,v 1.9 2001/05/17 14:14:27 tmm Exp $
%define name  pdnsd
%define ver      1.1.7a
%define rel 1
%define prefix  /usr
%define confdir /etc
%define distro Generic

Summary: A caching dns proxy for small networks or dialin accounts
Name: %{name}
Version: %ver
Release: %rel
Copyright: GPL
Group:  Daemons
Source: %{name}-%{ver}.tar.gz
URL: http://home.t-online.de/home/Moestl/
Vendor: Thomas Moestl
Distribution: %{distro}
Prefix: %{prefix} 
BuildRoot: /var/tmp/%{name}-%{ver}-%{rel}-rpm-buildroot

%description
pdnsd is a proxy DNS daemon with permanent (disk-)cache and the ability
to serve local records. It is designed to detect network outages or hangups
and to prevent DNS-dependent applications like Netscape Navigator from hanging.

%prep
%setup

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{prefix} --sysconfdir=%{confdir} --with-distribution=%{distro} --mandir=%{_mandir} --enable-specbuild=yes
%__make

%install
%__make DESTDIR=${RPM_BUILD_ROOT} install; \
cp -f file-list.base file-list ; \
CURDIR=`pwd`; cd ${RPM_BUILD_ROOT} ; \
FILES=$(find . | sed 's/^\.//' \
  | grep -v pdnsd.conf \
  | grep -v '/usr/doc' \
  | grep -v '/usr/share/doc' \
  | grep -v '/var') ;
for FILE in $FILES; do \
  if [ ! -d "$FILE" ] ; then \
    if echo $FILE | grep -v '\.gz$' | grep -q man ; then \
      FILE="$FILE.gz" ; \
    fi ; \
    echo $FILE >> $CURDIR/file-list ; \
  fi ; \
done

%clean
if [ -O "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" -a "$RPM_BUILD_ROOT" != "$HOME" ]; then
  echo "Deleting build root $RPM_BUILD_ROOT"
  rm -rf "$RPM_BUILD_ROOT"
fi
rm -rf ${RPM_BUILD_DIR}/%{name}-%{ver}

%files -f file-list

%post
if [ "%{distro}" = "SuSE" -a -w /etc/rc.config ]; then 
  grep "START_PDNSD" /etc/rc.config > /dev/null
  if [ $? -ne 0 ] ; then
    echo -e \
"\n\n#\n# Set to yes to start pdnsd at boot time\n#\nSTART_PDNSD=yes" \
>> /etc/rc.config
  fi
elif [ "%{distro}" = "RedHat" ]; then
  if [ $1 = 1 ]; then
    /sbin/chkconfig --add pdnsd
  fi
fi

%preun
if [ "%{distro}" = "RedHat" ]; then
  if [ $1 = 0 ]; then
    /sbin/chkconfig --del pdnsd
  fi
fi

%postun
if [ "%{distro}" = "RedHat" ]; then
  if [ $1 -ge 1 ]; then
    /sbin/service pdnsd condrestart >/dev/null 2>&1
  fi
fi

%changelog
* Sun May 16 2001 Thomas Moestl <tmoestl@gmx.net>
- Make use of chkconfig for Red Hat (patch by Christian Engstler)
* Sun Mar 25 2001 Thomas Moestl <tmoestl@gmx.net>
- Merged SuSE fixes by Christian Engstler
* Fri Feb 09 2001 Thomas Moestl <tmoestl@gmx.net>
- Merged in a spec fix for mapage inclusion contributed by Sourav K.
  Mandal
* Sun Nov 26 2000 Thomas Moestl <tmoestl@gmx.net>
- Added some patches contributed by Bernd Leibing
* Tue Aug 15 2000 Thomas Moestl <tmoestl@gmx.net>
- Added the distro for configure
* Tue Jul 11 2000 Sourav K. Mandal <smandal@mit.edu>
- autoconf/automake modifications