%include	/usr/lib/rpm/macros.perl
Summary:	A Mail Virus Scanner - Daemon.
Summary(pl):	Antywirusowy skaner poczty elektronicznej - Demon
Name:		amavisd
Version:	20010714
Release:	4
License:	GPL
Group:		Applications/Mail
Source0:	http://www.amavis.org/dist/perl/%{name}-snapshot-%{version}.tar.gz
Source1:	%{name}.init
URL:		http://www.amavis.org/
BuildRequires:	arc
BuildRequires:	autoconf
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
BuildRequires:	sh-utils
BuildRequires:	unarj
BuildRequires:	unrar
BuildRequires:	zoo
Obsoletes:	AMaViS
Obsoletes:	amavis
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
	--enable-smtp \
	--enable-all \
	--enable-syslog \
	--with-runtime-dir=%{_var}/spool/amavis/runtime \
	--with-virusdir=%{_var}/spool/amavis/virusmails \
	--with-logdir=%{_var}/log \
	--with-amavisuser=amavis \
	--with-sockname=%{_var}/run/amavisd/amavisd.sock

%{__make}

gzip -9nf README* NEWS AUTHORS BUGS ChangeLog FAQ HINTS TODO doc/amavis.html

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_var}/spool/amavis,%{_var}/run/amavisd}

%{__make} install \
	amavisuser=$(id -u) \
	DESTDIR=$RPM_BUILD_ROOT
install -D %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/amavisd
%attr(755,root,root) %{_sbindir}/amavis
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/*
%config(noreplace) %{_sysconfdir}/amavisd.conf
%doc *.gz doc/*.gz doc/amavis.png
%attr(750,amavis,root) %{_var}/spool/amavis
%attr(755,amavis,root) %{_var}/run/amavisd

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

%clean
rm -rf $RPM_BUILD_ROOT
