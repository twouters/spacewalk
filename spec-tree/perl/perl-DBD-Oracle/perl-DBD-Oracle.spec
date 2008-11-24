Summary: DBD-Oracle module for perl
Name: perl-DBD-Oracle
Version: 1.22
Release: 0%{?dist}
License:  GPL+ or Artistic
Group: Applications/CPAN
Source0: %{name}-%{version}.tar.gz
Url: http://www.cpan.org
BuildRoot: %{_tmppath}/perl-DBD-Oracle-buildroot/
BuildRequires: perl >= 0:5.6.1, perl-DBI
BuildRequires: oracle-instantclient-devel
BuildRequires: oracle-lib-compat
Requires: oracle-lib-compat
Requires: perl >= 0:5.6.1, oracle-instantclient-basic

%description
DBD-Oracle module for perl

%package explain
Summary: Oora_explain script from DBD-Oracle module for perl
Group: Applications/CPAN

%description explain
ora_explain script

%prep
%define modname %(echo %{name}| sed 's/perl-//')
%setup -q -n %{modname}-%{version} 

%build
eval $(perl -V:sitearch)
eval $(perl -V:vendorarch)
%ifarch i386
export ORACLE_HOME=/usr/lib/oracle/10.2.0.4/client
export LD_LIBRARY_PATH=/usr/lib/oracle/10.2.0.4/client/lib
export ORACLE_INCLUDE=/usr/include/oracle/10.2.0.4/client
%else
export ORACLE_HOME=/usr/lib/oracle/10.2.0.4/client64
export LD_LIBRARY_PATH=/usr/lib/oracle/10.2.0.4/client64/lib
export ORACLE_INCLUDE=/usr/include/oracle/10.2.0.4/client64
%endif

INCLUDES=$(echo -I$ORACLE_HOME/rdbms/public \
                -I$ORACLE_HOME/rdbms/demo \
                -I$ORACLE_HOME/network/public \
                -I$ORACLE_INCLUDE \
                -I$vendorarch/auto/DBI \
                -I$sitearch/auto/DBI)
# We can't trust the tests make by the Makefile.PL on modern Oracle installations
# because it leads to bloat, duble linking and inneficient relocation. It's a wonder
# it works at all
perl Makefile.PL -l \
    CC=gcc LD="gcc -v -Wl,-rpath,$ORACLE_HOME/lib" \
    CCFLAGS="-D_GNU_SOURCE" \
    PREFIX=$RPM_BUILD_ROOT/usr 
 make

%clean 
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
#kinda ugly but we need ORACLE_HOME to be set 
%if "%{_lib}" == "lib64"
export ORACLE_HOME=/usr/lib/oracle/10.2.0.4/client64/
%else
export ORACLE_HOME=/usr/lib/oracle/10.2.0.4/client/
%endif
eval `perl '-V:installarchlib'`
mkdir -p $RPM_BUILD_ROOT/$installarchlib
make install

[ -x /usr/lib/rpm/brp-compress ] && /usr/lib/rpm/brp-compress

find $RPM_BUILD_ROOT/usr -type f -print | 
    sed "s@^$RPM_BUILD_ROOT@@g" | 
    grep -E -v 'perllocal.pod|\.packlist|ora_explain' \
    > %{modname}-%{version}-filelist
if [ "$(cat %{modname}-%{version}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi
rm -f `find $RPM_BUILD_ROOT -type f -name perllocal.pod -o -name .packlist`

%files -f %{modname}-%{version}-filelist
%defattr(-,root,root)

%files explain
%defattr(-,root,root)
%{_bindir}/ora_explain
%{_mandir}/man1/ora_explain.1.gz

%changelog
* Tue Nov 25 2008 Miroslav Suchy <msuchy@redhat.com>
- added buildrequires for oracle-lib-compat
- rebased to DBD::Oracle 1.22
- removed DBD-Oracle-1.14-blobsyn.patch

* Thu Oct 16 2008 Milan Zazrivec 1.21-4
- bumped release for minor release tagging
- added %{?dist} to release

* Tue Aug 26 2008 Mike McCune 1.21-3
- Cleanup spec file to work in fedora and our new Makefile structure

* Wed Jul  2 2008 Michael Mraka <michael.mraka@redhat.com> 1.21-2
- rebased to DBD::Oracle 1.21, Oracle Instantclient 10.2.0.4
- ora_explain moved into subpackage

* Wed May 21 2008 Jan Pazdziora - 1.19-8
- rebuild on RHEL 4 as well.

* Fri Dec 05 2007 Michael Mraka <michael.mraka@redhat.com>
- update to DBD::Oracle 1.19 to support oracle-instantclient

* Fri Jun 20 2003 Mihai Ibanescu <misa@redhat.com>
- Linking against Oracle 9i Release 2 client libraries. 

* Sun Nov 11 2001 Chip Turner <cturner@redhat.com>
- update to DBD::Oracle 1.12 to fix LOB bug

* Mon Jul 23 2001 Cristian Gafton <gafton@redhat.com>
- compile against oracle libraries using -rpath setting
- disable as many checks as we can from the default Makefile.PL

* Mon Apr 30 2001 Chip Turner <cturner@redhat.com>
- Spec file was autogenerated. 
