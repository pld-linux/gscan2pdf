#
%include	/usr/lib/rpm/macros.perl
Summary:	A GUI to produce PDFs from scanned documents
Name:		gscan2pdf
Version:	0.9.27
Release:	1
License:	GPL
Group:		Applications/Publishing
Source0:	http://dl.sourceforge.net/gscan2pdf/%{name}-%{version}.tar.gz
# Source0-md5:	a3c8b674c66c74d945d5549a508a8344
Patch0:		%{name}-tesseract_polish.patch
Patch1:		%{name}-tessdata_prefix.patch
URL:		http://gscan2pdf.sourceforge.net/
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	perl-devel
BuildRequires:	rpm-perlprov >= 4.1-13
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
%patch1 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
rm -f $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
chmod -R u+w $RPM_BUILD_ROOT/*

desktop-file-install --delete-original  --vendor="" \
  --dir=$RPM_BUILD_ROOT%{_desktopdir}         \
  $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%find_lang %{name}

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc LICENCE
%attr(755,root,root) %{_bindir}/*
%{perl_vendorlib}/Gscan2pdf.pm
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_mandir}/man1/*.1*
