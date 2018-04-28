#!/usr/bin/tclsh

set arch "x86_64"
set base "cpp-driver-2.9.0"
set fileurl "https://github.com/datastax/cpp-driver/archive/2.9.0.tar.gz"

set var [list wget $fileurl -O $base.tar.gz]
exec >@stdout 2>@stderr {*}$var

if {[file exists build]} {
    file delete -force build
}

file mkdir build/BUILD build/RPMS build/SOURCES build/SPECS build/SRPMS
file copy -force $base.tar.gz build/SOURCES
file copy -force cassandra.pc.in build/SOURCES
file copy -force cassandra_static.pc.in build/SOURCES

set buildit [list rpmbuild --target $arch --define "_topdir [pwd]/build" -bb cassandra-cpp-driver.spec]
exec >@stdout 2>@stderr {*}$buildit

# Remove our source code
file delete $base.tar.gz
