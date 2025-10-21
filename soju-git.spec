Name:               soju
Version:            %{?tagged_version:%{tagged_version}}%{!?tagged_version:0}
Release:            0.%{?commitdate}.%{?shortcommit}%{?dist}
Summary:            A user-friendly IRC bouncer

License:            AGPL-3.0-or-later
URL:                https://soju.im

%global             upstream_base   https://codeberg.org/emersion/soju
%global             upstream        %{upstream_base}.git
%global             branch          master
%global             tag             %(git ls-remote --tags %{upstream} | grep -v '{}' | sort -V | tail -n1 | sed 's/.*\\///;s/^v//')
%global             commit          %(git ls-remote %{upstream} %{branch} | awk '{print $1}' | cut -c1-7)
%global             commitdate      %(date +%Y%m%d)
%global             shortcommit     %(echo %{commit} | cut -c1-7)

Version:            %{tag}+git%{shortcommit}
Source0:            %{upstream_base}/archive/%{commit}.tar.gz#/soju-%{commit}.tar.gz
Source1:            soju-sysusers.conf
Source2:            soju-tmpfiles.conf
Source3:            soju.service

Provides:           soju = %{version}-%{release}
Conflicts:          soju

BuildRequires:      git
BuildRequires:      go
BuildRequires:      sqlite-devel
BuildRequires:      scdoc

Suggests:           sqlite
Suggests:           postgresql

BuildRequires:      systemd-rpm-macros
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
soju is a user-friendly IRC bouncer. soju connects to upstream IRC servers on behalf of the user to provide extra functionality. soju supports many features such as multiple users, numerous IRCv3 extensions, chat history playback and detached channels. It is well-suited for both small and large deployments.

%prep
%autosetup -n %{name}-%{version}

%build
%make_build

%install
%make_install PREFIX=%{_prefix} DESTDIR=%{buildroot}
install -Dm0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/soju.conf
install -Dm0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/soju.conf
install -Dm0644 %{SOURCE3} %{buildroot}%{_unitdir}/soju.service
find %{buildroot}

%files
%license LICENSE
%doc README.md

%config(noreplace) /etc/soju/config

%{_sysusersdir}/soju.conf
%{_tmpfilesdir}/soju.conf
%{_unitdir}/soju.service

%{_bindir}/soju
%{_bindir}/sojuctl
%{_bindir}/sojudb

%{_mandir}/man1/soju.1*
%{_mandir}/man1/sojuctl.1*

%pre
%sysusers_create_compat %{_sysusersdir}/soju.conf

%post
%tmpfiles_create %{_tmpfilesdir}/soju.conf
%systemd_post soju.service

%preun
%systemd_preun soju.service

%postun
%systemd_postun_with_restart soju.service

%changelog
%autochangelog
