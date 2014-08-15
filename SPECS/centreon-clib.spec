%define cent_global_prefix /usr/local/centreon-full/

Name:		centreon-clib
Version:	1.4.0
Release:	1%{?dist}
Summary:	Centreon Clib

Group:		Centreon
License:	GPL
URL:		http://centreon.com
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	cmake28

%description
Centreon CLib %{version}

%prep
%setup -q


%build
cd build
cmake28 \
   -DWITH_TESTING=0 \
   -DWITH_PREFIX=%{cent_global_prefix} \
   -DWITH_SHARED_LIB=1 \
   -DWITH_STATIC_LIB=0 \
   -DWITH_PKGCONFIG_DIR=/usr/local/lib/pkgconfig .

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{cent_global_prefix}/lib" > %{buildroot}/etc/ld.so.conf.d/centreon-clib.conf

%clean
rm -rf %{buildroot}

%post
ldconfig


%files
%defattr(-,root,root,-)
/etc/ld.so.conf.d/centreon-clib.conf
%{cent_global_prefix}/include/com/centreon/clib.hh
%{cent_global_prefix}/include/com/centreon/clib/version.hh
%{cent_global_prefix}/include/com/centreon/concurrency/condvar.hh
%{cent_global_prefix}/include/com/centreon/concurrency/condvar_posix.hh
%{cent_global_prefix}/include/com/centreon/concurrency/condvar_win32.hh
%{cent_global_prefix}/include/com/centreon/concurrency/locker.hh
%{cent_global_prefix}/include/com/centreon/concurrency/mutex.hh
%{cent_global_prefix}/include/com/centreon/concurrency/mutex_posix.hh
%{cent_global_prefix}/include/com/centreon/concurrency/mutex_win32.hh
%{cent_global_prefix}/include/com/centreon/concurrency/read_locker.hh
%{cent_global_prefix}/include/com/centreon/concurrency/read_write_lock.hh
%{cent_global_prefix}/include/com/centreon/concurrency/read_write_lock_posix.hh
%{cent_global_prefix}/include/com/centreon/concurrency/read_write_lock_win32.hh
%{cent_global_prefix}/include/com/centreon/concurrency/runnable.hh
%{cent_global_prefix}/include/com/centreon/concurrency/semaphore.hh
%{cent_global_prefix}/include/com/centreon/concurrency/semaphore_posix.hh
%{cent_global_prefix}/include/com/centreon/concurrency/semaphore_win32.hh
%{cent_global_prefix}/include/com/centreon/concurrency/thread.hh
%{cent_global_prefix}/include/com/centreon/concurrency/thread_pool.hh
%{cent_global_prefix}/include/com/centreon/concurrency/thread_posix.hh
%{cent_global_prefix}/include/com/centreon/concurrency/thread_win32.hh
%{cent_global_prefix}/include/com/centreon/concurrency/write_locker.hh
%{cent_global_prefix}/include/com/centreon/delayed_delete.hh
%{cent_global_prefix}/include/com/centreon/exceptions/basic.hh
%{cent_global_prefix}/include/com/centreon/exceptions/interruption.hh
%{cent_global_prefix}/include/com/centreon/handle.hh
%{cent_global_prefix}/include/com/centreon/handle_action.hh
%{cent_global_prefix}/include/com/centreon/handle_listener.hh
%{cent_global_prefix}/include/com/centreon/handle_manager.hh
%{cent_global_prefix}/include/com/centreon/handle_manager_posix.hh
%{cent_global_prefix}/include/com/centreon/handle_manager_win32.hh
%{cent_global_prefix}/include/com/centreon/hash.hh
%{cent_global_prefix}/include/com/centreon/io/directory_entry.hh
%{cent_global_prefix}/include/com/centreon/io/file_entry.hh
%{cent_global_prefix}/include/com/centreon/io/file_stream.hh
%{cent_global_prefix}/include/com/centreon/library.hh
%{cent_global_prefix}/include/com/centreon/library_posix.hh
%{cent_global_prefix}/include/com/centreon/library_win32.hh
%{cent_global_prefix}/include/com/centreon/logging/backend.hh
%{cent_global_prefix}/include/com/centreon/logging/engine.hh
%{cent_global_prefix}/include/com/centreon/logging/file.hh
%{cent_global_prefix}/include/com/centreon/logging/logger.hh
%{cent_global_prefix}/include/com/centreon/logging/syslogger.hh
%{cent_global_prefix}/include/com/centreon/logging/temp_logger.hh
%{cent_global_prefix}/include/com/centreon/misc/argument.hh
%{cent_global_prefix}/include/com/centreon/misc/command_line.hh
%{cent_global_prefix}/include/com/centreon/misc/get_options.hh
%{cent_global_prefix}/include/com/centreon/misc/stringifier.hh
%{cent_global_prefix}/include/com/centreon/namespace.hh
%{cent_global_prefix}/include/com/centreon/process.hh
%{cent_global_prefix}/include/com/centreon/process_listener.hh
%{cent_global_prefix}/include/com/centreon/process_manager.hh
%{cent_global_prefix}/include/com/centreon/process_manager_posix.hh
%{cent_global_prefix}/include/com/centreon/process_manager_win32.hh
%{cent_global_prefix}/include/com/centreon/process_posix.hh
%{cent_global_prefix}/include/com/centreon/process_win32.hh
%{cent_global_prefix}/include/com/centreon/shared_ptr.hh
%{cent_global_prefix}/include/com/centreon/task.hh
%{cent_global_prefix}/include/com/centreon/task_manager.hh
%{cent_global_prefix}/include/com/centreon/timestamp.hh
%{cent_global_prefix}/include/com/centreon/unique_array_ptr.hh
%{cent_global_prefix}/include/com/centreon/unordered_hash.hh
%{cent_global_prefix}/lib/libcentreon_clib.so
/usr/local/lib/pkgconfig/centreon-clib.pc



%changelog
* Thu Aug 14 2014 Florent Peterschmitt <fpeterschmitt@capensis.fr>
- Init
