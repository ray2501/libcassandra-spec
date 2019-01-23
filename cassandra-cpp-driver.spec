Name:    cassandra-cpp-driver
Version: 2.11.0
Release: 0
Summary: DataStax C/C++ Driver for Apache Cassandra

Group: Development/Tools
License: Apache-2.0
URL: https://github.com/datastax/cpp-driver
Source0: cpp-driver-%{version}.tar.gz
Source1: cassandra.pc.in
Source2: cassandra_static.pc.in

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: cmake >= 2.6.4
BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: libuv-devel 
BuildRequires: openssl-devel >= 0.9.8e

%description
A modern, feature-rich, and highly tunable C/C++ client library for Apache
Cassandra using exclusively Cassandra's native protocol and Cassandra Query
Language.

%define lib_name libcassandra2

%package -n %{lib_name}
Summary:        Shared library from C/C++ Driver for Apache Cassandra
Group:          System/Libraries
Provides:       %{name} = %{version}
Obsoletes:      %{name} < %{version}

%description -n %{lib_name}
This package holds the shared library of C/C++ Driver for Apache Cassandra

%package devel
Summary: Development libraries for ${name}
Group: Development/Tools
Requires: %{name} = %{version}
Requires: libuv1
Requires: openssl >= 0.9.8e
Requires: pkgconfig
Requires: %{lib_name} = %{version}

%description devel
Development libraries for %{name}

%package devel-static
Summary: Development libraries for statically link ${name}
Group: Development/Tools
Requires: %{name} = %{version}
Requires: libuv1
Requires: openssl >= 0.9.8e
Requires: pkgconfig

%description devel-static
Development libraries for statically link {name}

%prep
%setup -qn cpp-driver-%{version}

%build
export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'
cmake -DCMAKE_BUILD_TYPE=RELEASE -DCASS_BUILD_STATIC=ON -DCASS_INSTALL_PKG_CONFIG=OFF -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_libdir} .
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}/%{_libdir}/pkgconfig
sed -e "s#@prefix@#%{_prefix}#g" \
    -e "s#@exec_prefix@#%{_exec_prefix}#g" \
    -e "s#@libdir@#%{_libdir}#g" \
    -e "s#@includedir@#%{_includedir}#g" \
    -e "s#@version@#%{version}#g" \
    %SOURCE1 > %{buildroot}/%{_libdir}/pkgconfig/cassandra.pc
sed -e "s#@prefix@#%{_prefix}#g" \
    -e "s#@exec_prefix@#%{_exec_prefix}#g" \
    -e "s#@libdir@#%{_libdir}#g" \
    -e "s#@includedir@#%{_includedir}#g" \
    -e "s#@version@#%{version}#g" \
    %SOURCE2 > %{buildroot}/%{_libdir}/pkgconfig/cassandra_static.pc

%clean
rm -rf %{buildroot}

%check
# make check

%post   -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README.md LICENSE.txt

%files -n %{lib_name}
%defattr(-,root,root,-)
%{_libdir}/libcassandra.so.%{version}
%{_libdir}/libcassandra.so.2

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/libcassandra.so
%{_libdir}/pkgconfig/cassandra.pc

%files devel-static
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/cassandra_static.pc
%{_libdir}/libcassandra_static.a

%changelog
* Mon Mar 13 2017 Michael Penick <michael.penick@datastax.com> - 2.6.0-1
- release
