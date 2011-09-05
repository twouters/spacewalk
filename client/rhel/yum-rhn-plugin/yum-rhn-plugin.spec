Summary: RHN support for yum
Name: yum-rhn-plugin
Version: 1.6.10
Release: 1%{?dist}
License: GPLv2
Group: System Environment/Base
Source0: https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
URL:     https://fedorahosted.org/spacewalk
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if %{?suse_version: %{suse_version} > 1110} %{!?suse_version:1}
BuildArch: noarch
%endif
BuildRequires: python
BuildRequires: intltool
BuildRequires: gettext

Requires: yum >= 3.2.19-15
Requires: rhn-client-tools >= 1.6.6-1
Requires: m2crypto >= 0.16-6
Requires: python-iniparse

# Not really, but for upgrades we need these
Requires: rhn-setup
Obsoletes: up2date < 5.0.0
Provides: up2date = 5.0.0

%description
This yum plugin provides support for yum to access a Red Hat Network server for
software updates.

%prep
%setup -q

%build
make -f Makefile.yum-rhn-plugin

%install
rm -rf $RPM_BUILD_ROOT
make -f Makefile.yum-rhn-plugin install VERSION=%{version}-%{release} PREFIX=$RPM_BUILD_ROOT MANPATH=%{_mandir} 

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# 682820 - re-enable yum-rhn-plugin after package upgrade if the system is already registered
export pluginconf='/etc/yum/pluginconf.d/rhnplugin.conf'
if [ $1 -gt 1 ] && [ -f /etc/sysconfig/rhn/systemid ] && [ -f "$pluginconf" ]; then
    if grep -q '^[[:space:]]*enabled[[:space:]]*=[[:space:]]*1[[:space:]]*$' \
       "$pluginconf"; then
        touch /var/tmp/enable-yum-rhn-plugin
    fi
fi

%post
# 682820 - re-enable yum-rhn-plugin after package upgrade if the system is already registered
export pluginconf='/etc/yum/pluginconf.d/rhnplugin.conf'
if [ $1 -gt 1 ] && [ -f "$pluginconf" ] && [ -f "/var/tmp/enable-yum-rhn-plugin" ]; then
    sed -i 's/^\([[:space:]]*enabled[[:space:]]*=[[:space:]]*\)0\([[:space:]]*\)$/\11\2/'  \
        "$pluginconf"
    rm -f /var/tmp/enable-yum-rhn-plugin
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/yum/pluginconf.d/rhnplugin.conf
%dir /var/lib/up2date
%{_mandir}/man*/*
%{_datadir}/yum-plugins/*
%{_datadir}/rhn/actions/*
%doc LICENSE

%changelog
* Mon Sep 05 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.10-1
- 734492, 734965, 735282 - check command line options only for yum

* Fri Aug 12 2011 Miroslav Suchý 1.6.9-1
- do not verify md5, size and mtime for /etc/yum/pluginconf.d/rhnplugin.conf

* Thu Aug 11 2011 Miroslav Suchý 1.6.8-1
- do not mask original error by raise in execption

* Fri Aug 05 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.7-1
- parse commandline on our own

* Thu Aug 04 2011 Miroslav Suchý 1.6.6-1
- 690616 - fail to rollback if target package is not available

* Thu Aug 04 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.5-1
- the latest yum-rhn-plugin and rhn-client-tools require each other

* Thu Aug 04 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.4-1
- 710065 - exception messages are in unicode

* Tue Aug 02 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.3-1
- fixed package exclusion
- 725496 - respect default plugin settings from [main]

* Tue Aug 02 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.2-1
- 701189 - make sure cachedir exists

* Mon Aug 01 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.1-1
- call conduit.getConf() only once
- 691283 - create persistdir in _repos_persistdir instead of PWD
- 684342 - beside repo.id, cache even repo.name
- disable network in cache only mode
- cache list of last seen channels so we can correctly clean them
- 627525 - disable network communication with certain commands/options
- reverted init_hook -> prereposetup_hook move
- Bumping package versions for 1.6.

* Tue Jul 19 2011 Jan Pazdziora 1.5.11-1
- Merging Transifex changes for yum-rhn-plugin.
- New translations from Transifex for yum-rhn-plugin.
- Download translations from Transifex for yum-rhn-plugin.

* Tue Jul 19 2011 Jan Pazdziora 1.5.10-1
- update .po and .pot files for yum-rhn-plugin

* Mon Jul 18 2011 Simon Lukasik <slukasik@redhat.com> 1.5.9-1
- 703169 - Search for cached repomd.xml in a correct path (slukasik@redhat.com)

* Tue Jul 12 2011 Jan Pazdziora 1.5.8-1
- Fixing sloppy coding.

* Tue Jun 28 2011 Miroslav Suchý 1.5.7-1
- 707241 - create progressbar even during groupinstall and do not delete
  rhnplugin.repos during groupinstall command (msuchy@redhat.com)

* Mon May 02 2011 Miroslav Suchý 1.5.6-1
- set proxy_dict only if we have some proxy
- proxy_dict is private attribute

* Fri Apr 29 2011 Miroslav Suchý 1.5.5-1
- code cleanup
- 691283 - create persistdir in _repos_persistdir instead of PWD
  (msuchy@redhat.com)

* Thu Apr 21 2011 Miroslav Suchý 1.5.4-1
- in rhel5 http_header is not present

* Wed Apr 20 2011 Miroslav Suchý 1.5.3-1
- rhel5 does not have _default_grabopts()

* Tue Apr 12 2011 Miroslav Suchý 1.5.2-1
- remove duplicate keyword (msuchy@redhat.com)

* Tue Apr 12 2011 Miroslav Suchý 1.5.1-1
- remove dead code
- use default headers from yum class YumRepository
- 690190 - yumdownloader set callbacks soon, save it to new repo
- Bumping package versions for 1.5

* Fri Apr 08 2011 Miroslav Suchý 1.4.15-1
- fix cs translation (msuchy@redhat.com)

* Fri Apr 08 2011 Miroslav Suchý 1.4.14-1
- update copyright years (msuchy@redhat.com)
- download spacewalk.yum-rhn-plugin from Transifex (msuchy@redhat.com)

* Wed Apr 06 2011 Simon Lukasik <slukasik@redhat.com> 1.4.13-1
- Removing packages.verifyAll capability; it was never used.
  (slukasik@redhat.com)
- Moving unit test for touchTimeStamp() which was moved to yum-rhn-plugin
  (slukasik@redhat.com)

* Wed Apr 06 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.12-1
- there're no opts when called from rhn_check

* Mon Apr 04 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.11-1
- 688870 - resolve --enablerepo/--disablerepo for RHN repos

* Fri Apr 01 2011 Miroslav Suchý 1.4.10-1
- 690234 - do not re-create repo if it exist and is type of RhnRepo

* Fri Apr 01 2011 Miroslav Suchý 1.4.9-1
- name of attribute have to be in apostrophe

* Wed Mar 30 2011 Miroslav Suchý 1.4.8-1
- 683200 - ssl cert can not be unicode string
- fix variable typo
- older yum do not have _repos_persistdir

* Wed Mar 30 2011 Miroslav Suchý <msuchy@redhat.com> 1.4.7-1
- 683200 - support IDN

* Thu Mar 24 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.6-1
- 688870 - also check whether cached repo is valid

* Wed Mar 23 2011 Jan Pazdziora 1.4.5-1
- remove every reference to "up2date --register" - even in comments
  (msuchy@redhat.com)
- 684342 - beside repo.id, cache even repo.name (msuchy@redhat.com)

* Thu Mar 10 2011 Miroslav Suchý <msuchy@redhat.com> 1.4.4-1
- 683546 - optparse isn't friendly to translations in unicode
- 682820 - re-enable yum-rhn-plugin after package upgrade if the system is
  already registered
- forward port translations from RHEL6 to yum-rhn-plugin

* Fri Feb 18 2011 Jan Pazdziora 1.4.3-1
- handle installations of less recent package versions correctly
  (mzazrivec@redhat.com)

* Wed Feb 16 2011 Miroslav Suchý <msuchy@redhat.com> 1.4.2-1
- l10n: Updates to Russian (ru) translation (ypoyarko@fedoraproject.org)
- repopulate package sack after initial setup (mzazrivec@redhat.com)

* Mon Feb 14 2011 Jan Pazdziora 1.4.1-1
- 675780 - remove installed packages from transaction (mzazrivec@redhat.com)
- 671032 - specify RHN as "RHN Satellite or RHN Classic" (msuchy@redhat.com)
- 671032 - disable rhnplugin by default and enable it only after successful
  registration (msuchy@redhat.com)
- Bumping package versions for 1.4 (tlestach@redhat.com)

* Wed Feb 02 2011 Tomas Lestach <tlestach@redhat.com> 1.3.6-1
- this was accidentaly commited in previous commit - reverting
  (msuchy@redhat.com)
- 648403 - do not require up2date on rhel5 (msuchy@redhat.com)

* Mon Jan 31 2011 Tomas Lestach <tlestach@redhat.com> 1.3.5-1
- 672471 - do not send info to rhnParent about removing packages if plugin is
  enabled, but machine is not registred - i.e. getSystemId() returns None
  (msuchy@redhat.com)

* Thu Jan 20 2011 Tomas Lestach <tlestach@redhat.com> 1.3.4-1
- updating Copyright years for year 2011 (tlestach@redhat.com)
- update .po and .pot files for yum-rhn-plugin (tlestach@redhat.com)
- 666545 - don't report empty transactions as a successful action
  (mzazrivec@redhat.com)
- fix expression semantics (mzazrivec@redhat.com)

* Fri Jan 14 2011 Michael Mraka <michael.mraka@redhat.com> 1.3.3-1
- switch off network communication in cache only mode
- cache list of rhn channels so we can correctly clean our stuff
- 627525 - moved communication with satellite server from init_hook to
- 656380 - do not disable SSL server name check for XMLRPC communication
- 652424 - code optimalization: use up2date_cfg as class atribute
- 652424 - do not enable Akamai if you set useNoSSLForPackages option
- 627525 - do not parse command line, leave it to yum itself

* Mon Jan 03 2011 Miroslav Suchý <msuchy@redhat.com> 1.3.2-1
- 666876 - respect metadata_expire setting from yum config

* Wed Nov 24 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.1-1
- removed unused imports

* Mon Nov 15 2010 Jan Pazdziora 1.2.7-1
- l10n: Updates to Italian (it) translation (tombo@fedoraproject.org)

* Wed Nov 10 2010 Jan Pazdziora 1.2.6-1
- call config.initUp2dateConfig() only once (msuchy@redhat.com)

* Tue Nov 02 2010 Jan Pazdziora 1.2.5-1
- Update copyright years in the rest of the repo.
- update .po and .pot files for yum-rhn-plugin

* Tue Oct 12 2010 Jan Pazdziora 1.2.4-1
- l10n: Updates to Persian (fa) translation (aysabzevar@fedoraproject.org)

* Wed Aug 25 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.3-1
- 626822 - packages for update should be cached

* Mon Aug 23 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.2-1
- 625778 - require newer yum-rhn-plugin

* Thu Aug 12 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.2.1-1
- update .po and .pot files for yum-rhn-plugin (msuchy@redhat.com)

* Tue Aug 10 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.6-1
- l10n: Italian version fully updated (fvalen@fedoraproject.org)

* Thu Aug 05 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.5-1
- enable caching for action packages.fullUpdate

* Tue Jul 20 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.4-1
- download scheduled package installation in advance (msuchy@redhat.com)
- add parameter cache_only to all client actions (msuchy@redhat.com)

* Mon Jun 14 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.3-1
- 598323 - yumex do not set version (msuchy@redhat.com)
- l10n: Updates to Chinese (China) (zh_CN) translation
  (leahliu@fedoraproject.org)
- l10n: Updates to Spanish (Castilian) (es) translation
  (gguerrer@fedoraproject.org)
- l10n: Updates to Russian (ru) translation (ypoyarko@fedoraproject.org)
- cleanup - removing translation file, which does not match any language code
  (msuchy@redhat.com)
- update po files for yum-rhn-plugin (msuchy@redhat.com)
- l10n: Updates to German (de) translation (ttrinks@fedoraproject.org)
- l10n: Updates to Polish (pl) translation (raven@fedoraproject.org)

* Wed May 05 2010 Justin Sherrill <jsherril@redhat.com> 1.1.2-1
- 589120 - fixing issue with traceback from rhn_chec "no attribute cfg"
  (jsherril@redhat.com)

* Mon Apr 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.1-1
- bumping spec files to 1.1 packages

* Thu Mar 25 2010 Jan Pazdziora 0.9.2-1
- channel_blacklist seems to be never used, removing

* Tue Feb 23 2010 Miroslav Suchý <msuchy@redhat.com> 0.9.1-1
- rebuild for rhel6

* Thu Feb 04 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.5-1
- updated copyrights

* Mon Jan 25 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.4-1
- fixed HTTP Error 401 Authorization Required on Fedora 12

* Fri Jan 15 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.3-1
- fixed syntax error

* Thu Jan 14 2010 Miroslav Suchý <msuchy@redhat.com> 0.8.2-1
- 549368 - yum now (F12) pass new attribute size, we should honor it if given

* Fri Dec 18 2009 Miroslav Suchý <msuchy@redhat.com> 0.8.1-1
- 504295 - retrieve and use debug level from rhncli, pass it to yum
- 548448 - when we are doing rollback, bypass dependecy resolution

* Tue Dec  1 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.8-1
- 437822 - python dependecy is not picked up automatically
- 437822 - when persistent enable/disable of rhn repo is requested, do it in rhnplugin.conf
- 514467 - when we say RHN is disabled, we may actually really disable it

* Wed Nov 25 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.7-1
- 527412 - compute delta and write it to logs only if writeChangesToLog is set to 1
- 527412 - Revert "fixing rhn-plugin to update package profiles through the updatePackageProfile call instead of manually setting up the delta as it causes stale package entries in the ui due to epoch being set to 0 for a no epoch packages"
- 509342 - explicitly say, that this is example
- 515575 - require recent rhn-client tools
- remove no.po as Norwegian translation is for some time in nb.po, which is correct location anyway
- remove double slash, Mandriva do not likes it
- fix build under opensuse

* Thu Oct  1 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.6-1
- change licence in header to correct GPLv2

* Wed Sep 30 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.5-1
- add LICENSE

* Tue Sep 29 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.4-1
- add source url
- add fix version in provides
- clean %%files section

* Thu Sep 17 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.2-1
- Rhpl was removed from rhel client packages
- use macros in spec file
- move rhnplugin from /var/lib/yum-plugins to /usr/share/yum-plugins - it is not executable
- versioned obsolete and provide the obsolete package
- Fix yum-rhn-plugin requiring a version of m2crypto that doesn't exist.
- bumping versions to 0.7.0

* Thu Aug 06 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.6.1-1
- fixing the changelog order causing tito build to fail (pkilambi@redhat.com)
- fixing date (pkilambi@redhat.com)
- new build (pkilambi@redhat.com)
- client tools merge from svn (pkilambi@redhat.com)

* Wed Aug 05 2009 Pradeep Kilambi <pkilambi@redhat.com>
- new build

* Mon Aug  3 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.4-13%{?dist}
- Resolves:  #514503

* Fri Jun 26 2009 John Matthews <jmatthew@redhat.com> 0.5.7-1
- yum-rhn-plugin requires m2crypto

* Thu Jun 25 2009 John Matthews <jmatthew@redhat.com> 0.5.6-1
- yum operations are not getting redirected as the GET requested is formed at
  the plugin level and not through rhnlib. (pkilambi@redhat.com)
- 467866 - Raise a more cleaner message if clients end up getting badStatusLine
  error due to 502 proxy errors (pkilambi@redhat.com)

* Mon Jun 22 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.4-10%{?dist}
- Resolves: #484245 

* Fri Jun 12 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.4-9%{?dist}
- Resolves: #467866

* Thu May 21 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.5-1
- merging additional spec changes and minor edits from svn (pkilambi@redhat.com)
- 467866 - catch the BadStatusLine and let use know that the server is
  unavailable temporarily (pkilambi@redhat.com)
- 489396 - remove limitation of rhn auth refresh for only 401 errors (jmatthew@redhat.com)
- Throw an InvalidRedirectionError if redirect url does'nt fetch the package
  (pkilambi@redhat.com)
- updating translations (pkilambi@redhat.com)
- 465340 - clean up loginAuth.pkl along with rest of the cache while yum clean
  all. This file should get recreated when the clients checks in with RHN
  again. (pkilambi@redhat.com)
- cleanup imports (pkilambi@redhat.com)
- 481042 - handle ssl timeout exceptions raised from m2crypto more gracefully (pkilambi@redhat.com)
- 448245 - adding a single global module level reference to yumAction so
  rhn_check uses this for all package related actions as a single instance
  instead of reloading yum configs each time (pkilambi@redhat.com)
- 491127 - fixing the package actions to  inspect the error codes and raise
  except (pkilambi@redhat.com)

* Tue May 12 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.4-7%{?dist}
- Resolves: #467866  #489396

* Fri May  8 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.4-4%{?dist}
- Resolves:  #441738 #444581 #465340 #481042 #481053 #491127 #476899

* Wed Jan 21 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.4-1
- Remove usage of version and sources files.

* Tue Nov 11 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.5.3-30%{?dist}
- Resolves: #470988

* Fri Oct 24 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.5.3-28%{?dist}
- Resolves: #467043

* Tue Oct 21 2008 John Matthews <jmatthews@redhat.com> - 0.5.3-27%{?dist}
- Updated rhn-client-tools requires to 0.4.19 or greater

* Thu Sep 18 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.5.3-26%{?dist}
- Resolves: #431082 #436043 #436804 #441265 #448012 #448044 #449726
- Resolves: #450241 #453690 #455759 #455760 #456540 #457191  #462499

* Wed Aug  6 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.5.3-20%{?dist}
- new build

* Tue Aug  5 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.5.3-12%{?dist}
- Resolves: #457190

* Tue May 20 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.5.3-12%{?dist}-
- new build

* Mon May 19 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.5.3-6
- Resolves: #447402

* Tue Mar 11 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.5.3-6
- Resolves: #438175

* Tue Mar 11 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.5.3-5
- Resolves: #435840

* Tue Mar 11 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.5.3-4
- Resolves: #433781

* Wed Jan 16 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.5.3-3
- Resolves: #222327, #226151, #245013, #248385, #251915, #324141 
- Resolves: #331001, #332011, #378911

* Fri Aug 17 2007 Pradeep Kilambi <pkilambi@redhat.com>  - 0.5.2-3
- Resolves: #232567

* Tue Jul 17 2007 Pradeep Kilambi <pkilambi@redhat.com> - 0.5.2-2
- Resolves: #250638

* Tue Jul 17 2007 James Slagle <jslagle@redhat.com> - 0.5.2-1
- Patch from katzj@redhat.com for yum 3.2.x compatibility
- Resolves: #243769

* Thu Jun 26 2007 Shannon Hughes <shughes@redhat.com> - 0.5.1-2
- Resolves: #232567, #234880, #237300

* Thu Dec 14 2006 John Wregglesworth <wregglej@redhat.com> - 0.3.1-1
- Updated translations.
- Related: #216835

* Wed Dec 13 2006 James Bowes <jbowes@redhat.com> - 0.3.0-2
- Add requires for rhn-setup.
- Related: #218617

* Mon Dec 11 2006 James Bowes <jbowes@redhat.com> - 0.3.0-1
- Updated translations.
- Related: #216835

* Tue Dec 05 2006 James Bowes <jbowes@redhat.com> - 0.2.9-1
- Updated translations.

* Fri Dec 01 2006 James Bowes <jbowes@redhat.com> - 0.2.8-1
- Updated translations.

* Thu Nov 30 2006 James Bowes <jbowes@redhat.com> - 0.2.7-1
- New and updated translations.

* Tue Nov 28 2006 James Bowes <jbowes@redhat.com> - 0.2.6-1
- Reauthenticate with RHN if the session expires.
- Resolves: #217706

* Tue Nov 28 2006 James Bowes <jbowes@redhat.com> - 0.2.5-1
- New and updated translations.

* Mon Nov 20 2006 James Bowes <jbowes@redhat.com> - 0.2.4-1
- Fix for #215602

* Mon Nov 13 2006 James Bowes <jbowes@redhat.com> - 0.2.3-1
- Add man pages.

* Fri Nov 03 2006 James Bowes <jbowes@redhat.com> - 0.2.2-1
- Fix for #213793

* Mon Oct 30 2006 James Bowes <jbowes@redhat.com> - 0.2.1-1
- New translations.
- Fixes for #212255, #213031, #211568

* Tue Oct 25 2006 James Bowes <jbowes@redhat.com> - 0.2.0-1
- Use sslCACert rather than sslCACert[0]. Related to #212212.

* Tue Oct 24 2006 James Bowes <jbowes@redhat.com> - 0.1.9-3
- add BuildRequires: gettext

* Tue Oct 24 2006 James Bowes <jbowes@redhat.com> - 0.1.9-2
- add BuildRequires: intltool

* Tue Oct 24 2006 James Bowes <jbowes@redhat.com> - 0.1.9-1
- fixes for #181830, #208852, #206941

* Tue Oct 24 2006 James Bowes <jbowes@redhat.com> - 0.1.8-1
- Require a version of rhn-client-tools that doesn't provide up2date.
- package the translation files.

* Fri Oct 13 2006 James Bowes <jbowes@redhat.com> - 0.1.7-2
- Obsolete up2date

* Wed Oct 11 2006 James Bowes <jbowes@redhat.com> - 0.1.7-1
- New version.
- Don't always assume we have an optparser.

* Thu Oct 05 2006 James Bowes <jbowes@redhat.com> - 0.1.6-1
- New version.

* Fri Sep 15 2006 James Bowes <jbowes@redhat.com> - 0.1.5-1
- Require rhpl for translation.

* Thu Sep 14 2006 James Bowes <jbowes@redhat.com> - 0.1.0-1
- New version.
- Require rhn-client-tools >= 0.1.4.
- Stop ghosting pyo files.

* Thu Aug 10 2006 James Bowes <jbowes@redhat.com> - 0.0.9-1
- New version.
- Fix for bz #202091 pirut crashes after installing package

* Mon Aug 07 2006 James Bowes <jbowes@redhat.com> - 0.0.8-2
- Set gpg checking from the plugin's config.

* Thu Aug 03 2006 James Bowes <jbowes@redhat.com> - 0.0.8-1
- New version.

* Mon Jul 31 2006 James Bowes <jbowes@redhat.com> - 0.0.7-1
- New version.

* Mon Jul 31 2006 James Bowes <jbowes@redhat.com> - 0.0.6-1
- Fix for bz #200697 – yum-rhn-plugin causes yum to fail
  under rhel5-server

* Thu Jul 27 2006 James Bowes <jbowes@redhat.com> - 0.0.5-1
- New version.

* Thu Jul 20 2006 James Bowes <jbowes@redhat.com> - 0.0.4-1
- New version.

* Wed Jul 19 2006 James Bowes <jbowes@redhat.com> - 0.0.3-3
- Correct buildroot location.

* Wed Jul 19 2006 James Bowes <jbowes@redhat.com> - 0.0.3-2
- Spec file cleanups.

* Wed Jul 12 2006 James Bowes <jbowes@redhat.com> - 0.0.3-1
- Install the packages action.

* Thu May 18 2006 James Bowes <jbowes@redhat.com> - 0.0.2-1
- Make Evr checking on rhn packages more exact.

* Mon Apr 17 2006 James Bowes <jbowes@redhat.com> - 0.0.1-2
- Update requirements for yum >= 2.9.0

* Tue Feb 28 2006 James Bowes <jbowes@redhat.com> - 0.0.1-1
- Initial version.
