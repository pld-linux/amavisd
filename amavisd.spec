%include	/usr/lib/rpm/macros.perl    
Summary:	A Mail Virus Scanner - Daemon.
Summary(pl):	Antywirusowy skaner poczty elektronicznej - Demon
Name:		amavisd
Version:	20010714
Release:	1
URL:		http://www.amavis.org/
Source0:	http://www.amavis.org/dist/perl/%{name}-snapshot-%{version}.tar.gz
Source1:	%{name}.init
License:	GPL
Group:		Applications/Mail
Group(de):	Applikationen/Post
Group(pl):	Aplikacje/Poczta
Group(pt):	Aplicações/Correio Eletrônico
Obsoletes:	AMaViS
Obsoletes:	amavis
BuildRequires:	autoconf >= 2.52
BuildRequires:	perl
BuildRequires:	perl-modules
BuildRequires:	perl-Convert-UUlib
BuildRequires:	perl-Convert-TNEF
BuildRequires:	perl-Unix-Syslog
BuildRequires:	perl-Archive-Tar
BuildRequires:	perl-Archive-Zip
BuildRequires:	perl-Compress-Zlib
BuildRequires:	perl-MIME-tools
BuildRequires:	file
BuildRequires:	sh-utils
BuildRequires:	arc
BuildRequires:	bzip2
BuildRequires:	lha
BuildRequires:	unarj
BuildRequires:	ncompress
BuildRequires:	unrar
BuildRequires:	zoo
Requires:	file
Requires:	sh-utils
Requires:	arc
Requires:	bzip2
Requires:	lha
Requires:	unarj
Requires:	ncompress
Requires:	unrar
Requires:	zoo
Requires:	%{_sbindir}/sendmail
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners. This is daemonized version of amavis.

%description -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych. Wersja zdemonizowana.

%prep
%setup -q -n %{name}-snapshot-%{version}

%build
autoconf
%configure \
	--enable-postfix \
	--enable-smtp \
	--with-sendmail-wrapper=%{_sbindir}/sendmail \
	--with-runtime-dir=/tmp \
	--with-virusdir=/var/spool/amavis/virusmails \
	--with-sockname=/var/run/amavisd/amavisd.sock \
	--with-mailto="postmaster" \
	--with-amavisuser=amavis

%{__make}

gzip -9nf README* AUTHORS BUGS ChangeLog FAQ HINTS TODO doc/amavis.html

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/spool/amavis,/var/run/amavisd}

%{__make} install \
	amavisuser=$(id -u) \
	DESTDIR=$RPM_BUILD_ROOT
install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/amavisd
%attr(755,root,root) %{_sbindir}/amavis
%attr(754,root,root) /etc/rc.d/init.d/*
%config %{_sysconfdir}/amavisd.conf 
%doc *.gz doc/*.gz doc/amavis.png
%attr(770,amavis,root) /var/spool/amavis
%attr(755,amavis,root) /var/run/amavisd

%pre
if [ -n "`id -u amavis 2>/dev/null`" ]; then
        if [ "`id -u amavis`" != "97" ]; then
                echo "Warning: user amavis haven't uid=97. Correct this before installing amavis" 1>&2
                exit 1
        fi
else
        /usr/sbin/useradd -u 97 -r -d /var/spool/amavis  -s /bin/false -c "Anti Virus Checker" -g nobody  amavis 1>&2
fi

%postun
if [ "$1" = "0" ]; then
        /usr/sbin/userdel amavis
fi

%post
/sbin/chkconfig --add amavisd

if [ -f /var/lock/subsys/amavisd ]; then
        /etc/rc.d/init.d/amavisd restart >&2
else
        echo "Run \"/etc/rc.d/init.d/amavisd start\" to start Amavisd daemon."
fi

%preun
if [ "$1" = "0" ];then
        if [ -f /var/lock/subsys/amavisd ]; then
                /etc/rc.d/init.d/amavisd stop >&2
        fi
        /sbin/chkconfig --del amavisd
fi

%clean
rm -rf $RPM_BUILD_ROOT
