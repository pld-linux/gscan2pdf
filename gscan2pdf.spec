#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
Summary:	A GUI to produce PDFs from scanned documents
Name:		gscan2pdf
Version:	0.9.31
Release:	1
License:	GPL
Group:		Applications/Publishing
Source0:	http://downloads.sourceforge.net/gscan2pdf/%{name}-%{version}.tar.gz
# Source0-md5:	e92ee7b07ffd3543faf8a64940ad65dc
Patch0:		%{name}-tesseract_polish.patch
URL:		http://gscan2pdf.sourceforge.net/
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-devel
%{?with_tests:BuildRequires:	perl-Test-Pod}
BuildRequires:	perl-devel
BuildRequires:	rpm-perlprov >= 4.1-13
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	ImageMagick
Requires:	ImageMagick-perl
Requires:	djvulibre
Suggests:	gocr
Suggests:	sane-backends >= 1.0.17
Suggests:	sane-frontentds
Suggests:	tesseract
Suggests:	unpaper
Suggests:	xdg-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Only two clicks are required to scan several pages and then save all
or a selection as a PDF file, including metadata if required.

gscan2pdf can control regular or sheet-fed (ADF) scanners with SANE
via scanimage or scanadf, and can scan multiple pages at once. It
presents a thumbnail view of scanned pages, and permits simple
operations such as rotating and deleting pages.

PDF conversion is done by PDF::API2.

The resulting document may be saved as a PDF or a multipage TIFF file.

%prep
%setup -q
%patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
%{__rm} $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
chmod -R u+w $RPM_BUILD_ROOT/*

install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable
mv $RPM_BUILD_ROOT%{_datadir}/pixmaps/gscan2pdf.svg \
   $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable

desktop-file-install --delete-original  --vendor="" \
  --dir=$RPM_BUILD_ROOT%{_desktopdir}         \
  $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null ||:
%update_icon_cache hicolor

%postun
update-desktop-database &> /dev/null ||:
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc LICENCE
%attr(755,root,root) %{_bindir}/gscan2pdf
%attr(755,root,root) %{_bindir}/scanadf-perl
%attr(755,root,root) %{_bindir}/scanimage-perl
%{perl_vendorlib}/Gscan2pdf.pm
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_mandir}/man1/*.1*
%{_iconsdir}/hicolor/scalable/gscan2pdf.svg
