%global debug_package %{nil}
%global repo_name xone

Name:           xone-dkms
Version:        0.5.8
Release:        1%{?dist}
Summary:        Linux kernel driver for Xbox One and Xbox Series X|S accessories
Group:          System Environment/Kernel
License:        GPLv2
URL:            https://github.com/dlundqvist/xone
Source0:        %{repo_name}-%{version}.tar.gz

# Mapping Debian 'Depends' to RPM
BuildArch:      noarch
Requires:       dkms >= 2.1.0.0
Requires:       make
# Fedora/AlmaLinux equivalent of linux-headers-generic
Requires:       kernel-devel

Provides:       xone-modules = %{version}

%description
This driver supports Xbox One and Xbox Series X|S accessories including
wired controllers, the Xbox Wireless Adapter, and various third-party
controllers. It serves as a modern replacement for xpad and implements
Microsoft's Game Input Protocol (GIP).

Features include force feedback, rumble, battery status reporting, LED
control, and audio support.

This package uses DKMS to automatically build the xone kernel modules.

%prep
%setup -q -n %{repo_name}-%{version}

%build
# Nothing to build at RPM creation time; DKMS handles it on the target system.

%install
# Create the DKMS source directory
%global dkms_source_dir %{_usrsrc}/%{repo_name}-%{version}
mkdir -p %{buildroot}%{dkms_source_dir}

# Copy all source files for DKMS
cp -r ./* %{buildroot}%{dkms_source_dir}

# Remove the rpm directory from the installed source to keep it clean
rm -rf %{buildroot}%{dkms_source_dir}/rpm

%post
# Register and build the module using DKMS
dkms add -m %{repo_name} -v %{version} --rpm_safe_upgrade || :
dkms build -m %{repo_name} -v %{version} || :
dkms install -m %{repo_name} -v %{version} || :

%preun
# Remove the module from DKMS before uninstalling
dkms remove -m %{repo_name} -v %{version} --all --rpm_safe_upgrade || :

%files
%license LICENSE
%doc README.md
%{_usrsrc}/%{repo_name}-%{version}

%changelog
* Sat Apr 25 2026 Jacob Chisholm <jacob@example.com> - 0.0.1-1
- Initial adaptation from Debian xone-dkms config
- Targeted for Fedora 40 and AlmaLinux 10
