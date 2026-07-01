%global debug_package %{nil}
%global puppeteer_version %{__puppeteer_version}
%global chromium_version %{__chromium_version}
%global save_svg_as_png_version %{__save_svg_as_png_version}

Name:    redborder-webui-node-modules
Version: %{__version}
Release: %{__release}%{?dist}
Summary: redborder-webui node modules Package

License: MIT
URL: https://github.com/redBorder/redborder-webui-node-modules/
Source0: %{name}-%{version}.tar.gz

BuildRequires: nodejs >= 16 npm wget unzip
Requires: bash
AutoReqProv: no

%description
This RPM package bundles all necessary Node modules and Chromium binaries 
required for offline installation of redborder-webui. It uses puppeteer‑core 
to allow custom browser management.

%prep
%setup -qn %{name}-%{version}

%build
npm init -y
npm install puppeteer@%{puppeteer_version}
npm install save-svg-as-png@%{save_svg_as_png_version}

wget --no-check-certificate \
  https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/%{chromium_version}/chrome-linux.zip \
  -O chrome-linux-%{chromium_version}.zip
unzip chrome-linux-%{chromium_version}.zip -d chrome-linux
rm -f chrome-linux-%{chromium_version}.zip

%install
mkdir -p %{buildroot}/etc/profile.d
install -D -m 0644 resources/node-modules.sh %{buildroot}/etc/profile.d/node-modules.sh
mkdir -p %{buildroot}/var/www/rb-rails/node_modules/
cp -r node_modules/* %{buildroot}/var/www/rb-rails/node_modules/

mkdir -p %{buildroot}/var/www/rb-rails/.cache/puppeteer/chrome/linux-%{chromium_version}/
cp -r chrome-linux/* %{buildroot}/var/www/rb-rails/.cache/puppeteer/chrome/linux-%{chromium_version}/

%clean
rm -rf %{buildroot}

%files
%defattr(0755,root,root)
/etc/profile.d/node-modules.sh

%defattr(-,webui,webui)
/var/www/rb-rails/node_modules/
/var/www/rb-rails/.cache/puppeteer/

%changelog
* Fri Mar 28 2025 Daniel C. Cruz <dcastro@redborder.com>
- add environment variable to specify the correct puppeteer cache path
* Tue Jul 09 2024 Daniel C. Cruz <dcastro@redborder.com>
- first spec version