%include	/usr/lib/rpm/macros.perl
Summary:	A Mail Virus Scanner - Daemon.
Summary(pl):	Antywirusowy skaner poczty elektronicznej - Demon
Name:		amavisd
Version:	20010714
Release:	8
License:	GPL
Group:		Applications/Mail
Source0:	http://www.amavis.org/dist/perl/%{name}-snapshot-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-notest-mta.patch
Patch1:		%{name}-nomilter.patch
Patch2:		%{name}-qmail.patch
Patch3:		%{name}-mks_vir.patch
URL:		http://www.amavis.org/
BuildRequires:	arc
BuildRequires:	autoconf
BuildRequires:  automake
BuildRequires:	bzip2
BuildRequires:	file
BuildRequires:	lha
BuildRequires:	ncompress
BuildRequires:	perl-Archive-Tar
BuildRequires:	perl-Archive-Zip
BuildRequires:	perl-Compress-Zlib
BuildRequires:	perl-MIME-tools
BuildRequires:	perl-Unix-Syslog
BuildRequires:	perl-Convert-UUlib
BuildRequires:	perl-Convert-TNEF
BuildRequires:	perl-libnet
BuildRequires:	sh-utils
BuildRequires:	unarj
BuildRequires:	unrar
BuildRequires:	zoo
Requires:	%{_libdir}/sendmail
Requires:	arc
Requires:	bzip2
Requires:	file
Requires:	lha
Requires:	ncompress
Requires:	sh-utils
Requires:	unarj
Requires:	unrar
Requires:	zoo
Requires:	amavisd-daemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	AMaViS
Obsoletes:	amavis

%description
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners. This is daemonized version of amavis.

%description -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych. Wersja zdemonizowana.

%package postfix
Summary:	A Mail Virus Scanner - postfix back-end.
Summary(pl):	Antywirusowy skaner poczty elektronicznej - back-end dla postfiksa
Group:		Applications/Mail
Provides:	amavisd-daemon
Obsoletes:	amavisd-daemon
Requires:	postfix

%description postfix
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners. This is daemonized version of amavis.

This package contains backend for postfix.

%description postfix -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych. Wersja zdemonizowana.

Pakiet ten zawiera back-end dla postfiks.

%package exim
Summary:	A Mail Virus Scanner - exim backend.
Summary(pl):	Antywirusowy skaner poczty elektronicznej - backend dla exima
Group:		Applications/Mail
Provides:	amavisd-daemon
Obsoletes:	amavisd-daemon
Requires:	exim

%description exim
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners. This is daemonized version of amavis.

This package contains backend for exim.

%description exim -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych. Wersja zdemonizowana.

Pakiet ten zawiera back-end dla exima.

%package qmail
Summary:	A Mail Virus Scanner - qmail backend.
Summary(pl):	Antywirusowy skaner poczty elektronicznej - backend dla qmaila
Group:		Applications/Mail
Provides:	amavisd-daemon
Obsoletes:	amavisd-daemon
Requires:	qmailmta

%description qmail
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners. This is daemonized version of amavis.

This package contains backend for qmail.

%description qmail -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych. Wersja zdemonizowana.

Pakiet ten zawiera back-end dla qmaila.

%package sendmail
Summary:	A Mail Virus Scanner - sendmail backend.
Summary(pl):	Antywirusowy skaner poczty elektronicznej - backend dla sendmaila
Group:		Applications/Mail
Provides:	amavisd-daemon
Obsoletes:	amavisd-daemon
Requires:	sendmail

%description sendmail
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners. This is daemonized version of amavis.

This package contains backend for sendmail.

%description sendmail -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych. Wersja zdemonizowana.

Pakiet ten zawiera back-end dla sendmaila.

%prep
%setup -q -n %{name}-snapshot-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
aclocal
autoconf
automake -a -c -f
%configure \
	--enable-smtp \
	--enable-postfix \
	--enable-all \
	--enable-syslog \
	--with-runtime-dir=%{_var}/spool/amavis/runtime \
	--with-virusdir=%{_var}/spool/amavis/virusmails \
	--with-logdir=%{_var}/log \
	--with-amavisuser=amavis \
	--with-sockname=%{_var}/run/amavisd/amavisd.sock

%{__make}
mv amavis/amavisd amavis/amavisd.postfix

%configure \
	--disable-smtp \
	--enable-exim \
	--enable-all \
	--enable-syslog \
	--with-runtime-dir=%{_var}/spool/amavis/runtime \
	--with-virusdir=%{_var}/spool/amavis/virusmails \
	--with-logdir=%{_var}/log \
	--with-amavisuser=amavis \
	--with-sockname=%{_var}/run/amavisd/amavisd.sock

%{__make}
mv amavis/amavisd amavis/amavisd.exim

%configure \
	--disable-smtp \
	--enable-qmail \
	--enable-all \
	--enable-syslog \
	--with-runtime-dir=%{_var}/spool/amavis/runtime \
	--with-virusdir=%{_var}/spool/amavis/virusmails \
	--with-logdir=%{_var}/log \
	--with-amavisuser=amavis \
	--with-sockname=%{_var}/run/amavisd/amavisd.sock

%{__make}
mv amavis/amavisd amavis/amavisd.qmail

%configure \
	--disable-smtp \
	--enable-sendmail \
	--enable-all \
	--enable-syslog \
	--with-runtime-dir=%{_var}/spool/amavis/runtime \
	--with-virusdir=%{_var}/spool/amavis/virusmails \
	--with-logdir=%{_var}/log \
	--with-amavisuser=amavis \
	--with-sockname=%{_var}/run/amavisd/amavisd.sock

%{__make}
mv amavis/amavisd amavis/amavisd.sendmail

gzip -9nf README* NEWS AUTHORS BUGS ChangeLog FAQ HINTS TODO doc/amavis.html

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_var}/spool/amavis,%{_var}/run/amavisd}

%{__make} install \
	amavisuser=$(id -u) \
	DESTDIR=$RPM_BUILD_ROOT
install -D %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

install amavis/amavisd.{exim,postfix,qmail,sendmail} $RPM_BUILD_ROOT%{_sbindir}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/amavis
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/*
%config(noreplace) %{_sysconfdir}/amavisd.conf
%doc *.gz doc/*.gz doc/amavis.png
%attr(750,amavis,root) %{_var}/spool/amavis
%attr(755,amavis,root) %{_var}/run/amavisd

%files exim
%attr(755,root,root) %{_sbindir}/amavisd.exim
%ghost %{_sbindir}/amavisd

%files postfix
%attr(755,root,root) %{_sbindir}/amavisd.postfix
%ghost %{_sbindir}/amavisd

%files qmail
%attr(755,root,root) %{_sbindir}/amavisd.qmail
%ghost %{_sbindir}/amavisd

%files sendmail
%attr(755,root,root) %{_sbindir}/amavisd.sendmail
%ghost %{_sbindir}/amavisd

%pre
if [ -n "`id -u amavis 2>/dev/null`" ]; then
        if [ "`id -u amavis`" != "97" ]; then
                echo "Warning: user amavis haven't uid=97. Correct this before installing amavis" 1>&2
                exit 1
        fi
else
        %{_sbindir}/useradd -u 97 -r -d %{_var}/spool/amavis  -s /bin/false -c "Anti Virus Checker" -g nobody  amavis 1>&2
fi

%postun
if [ "$1" = "0" ]; then
        %{_sbindir}/userdel amavis
fi

%post
/sbin/chkconfig --add amavisd

if [ -f %{_var}/lock/subsys/amavisd ]; then
        /etc/rc.d/init.d/amavisd restart >&2
else
        echo "Run \"/etc/rc.d/init.d/amavisd start\" to start Amavisd daemon."
fi

%preun
if [ "$1" = "0" ];then
        if [ -f %{_var}/lock/subsys/amavisd ]; then
                /etc/rc.d/init.d/amavisd stop >&2
        fi
        /sbin/chkconfig --del amavisd
fi

%post exim
ln -sf amavisd.exim %{_sbindir}/amavisd

%post postfix
ln -sf amavisd.postfix %{_sbindir}/amavisd

%post qmail
ln -sf amavisd.qmail %{_sbindir}/amavisd

%post sendmail
ln -sf amavisd.sendmail %{_sbindir}/amavisd

%clean
rm -rf $RPM_BUILD_ROOT
