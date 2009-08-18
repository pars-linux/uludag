# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of
# the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS
# IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
# implied. See the License for the specific language governing
# rights and limitations under the License.
#
# The Initial Developer of the Original Code is Everything Solved.
# Portions created by Everything Solved are Copyright (C) 2007
# Everything Solved. All Rights Reserved.
#
# The Original Code is the Bugzilla Bug Tracking System.
#
# Contributor(s): Max Kanat-Alexander <mkanat@bugzilla.org>
# Translator(s):  Necmettin Begiter <necmettin@pardus.org.tr> (Turkish)

# This file contains a single hash named %strings, which is used by the
# installation code to display strings before Template-Toolkit can safely
# be loaded.
#
# Each string supports a very simple substitution system, where you can
# have variables named like ##this## and they'll be replaced by the string
# variable with that name.
#
# Please keep the strings in alphabetical order by their name.

%strings = (
    any  => 'herhangi bir',
    blacklisted => '(kara listede)',
    checking_for => 'Kontrol ediliyor',
    checking_dbd      => 'Kurulu perl DBD modülleri aranıyor...',
    checking_optional => 'Aşağıdaki Perl modülleri tercihe bağlı:',
    checking_modules  => 'Perl modülleri aranıyor...',
    done => 'tamamlandı.',
    header => "* Perl ##perl_ver## üzerinde Bugzilla ##bz_ver##\n"
            . "* ##os_name## ##os_ver## üzerinde çalışıyor",
    install_all => <<EOT,

İster gerekli, ister tercihe bağlı olsun, tüm modüllerin otomatik kurulumu için:

  ##perl## install-module.pl --all

EOT
    install_data_too_long => <<EOT,
UYARI: ##table##.##column## sütunundaki verinin bir kısmı yeni uzunluk sınırından (##max_length##) daha uzun. Düzeltilmesi gereken veri önce ##id_column## sütununun değeri, ardından da ##column## sütununun değeri olarak aşağıya listelenmiştir:

EOT
    install_module => '##module## sürüm ##version## yükleniyor...',
    max_allowed_packet => <<EOT,
UYARI: MySQL konfigürasyon dosyasında  max_allowed_packet parametresini
en az ##needed## olacak şekilde düzenlemelisiz. Şu anki değer: ##current##.
MySQL konfigürasyon dosyasındaki [mysqld] kısmında gerekli düzenlemeyi yapabilirsiniz.
EOT
    module_found => "s##ver## bulundu",
    module_not_found => "bulunamadı",
    module_ok => 'tamam',
    module_unknown_version => "bilinmeyen bir sürüm bulundu",
    template_precompile   => "Şablonlar ön-derleniyor...",
    template_removing_dir => "Varolan derlenmiş şablonlar kaldırılıyor...",
);

1;
