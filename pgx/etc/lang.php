<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

	define ("WARN_WRONG_PASS",	"Kullanıcı Adı ya da Parola Hatalı !!");
	define ("CONNECTION_ERROR",	"Bağlantı Hatası : ");
	define ("DBCONERROR",		"Veritabanı sunucusuna bağlanamadım.");
	define ("ERRORMESSAGE",		"Hata Mesajı : ");
	define ("ERRORNUM",		"Hata No : ");
        define ("ERROR",                "HATA");
        define ("CONFLICT_ERROR",       "Çakışma hatası !!");
        define ("SENDMAIL_ERROR",       "Mail gönderme sırasında Hata!!");
        define ("WRONG_ENTRY",          "Bu girdi size ait değil ya da sistemden kaldırılmış !!");
        define ("FILE_NOT_FOUND",       "Ulaşmak istediğiniz dosya bulunamadı, böyle bir dosya sistemde yok ya da kaldırılmış. Linkin doğru olduğuna eminseniz yönetim ile irtibata geçiniz.");
        define ("DISK_ERROR",           "Belirtilen içerik sisteme eklenemedi. Disk hatası meydana geldi. Verilen konum hatalı ya da disk dolmuş olabilir.");
        define ("DB_ERROR",             "Belirtilen içerik sisteme eklenemedi. Veritabanı ile ilgili bir hata meydana geldi.");
        define ("NOT_FOUND",            "Kriterlerinize uygun kayıt bulunamadı, bu kriterlere uyan kayıt bulunmaması bu donanımın Pardus ürünleri üzerinde çalışmayacağını göstermez.");
        define ("MAINLINK",             "<br><a href=\"{$config['core']['url']}\"> « Ana Sayfa </a>");
	define ("LOGIC_ERROR",		"Mantıksal Hata !!");
	define ("WELCOME",		"Hoşgeldiniz");
	define ("DOYOUAGREE",		"Onaylıyor musunuz ?");
	define ("NO_RECORD",		"Kayıt yok");
        define ("NO_QUEUE",		"Onay bekleyen kayıt yok!!");
	define ("ADMIN",		"Yetkili");
	define ("GROUPS",		"Gruplar");
	define ("CHOICE",		"Seçim");
	define ("OK",			"Tamam");
	define ("ADD",			"Ekle");
	define ("CLEAN",		"Temizle");
	define ("DELETE",		"Sil");
	define ("EDIT",			"Düzenle");
	define ("USERNAME",		"Kullanıcı Adı : ");
	define ("PASSWORD",		"Parola : ");
	define ("LOGIN",		"Giriş");
        define ("USER_EXIST",           "Seçtiğiniz Kullanıcı Adı ile kayıtlı bir kullanıcı mevcut");
        define ("REGISTER_OK",          "Kaydınız alındı, kayıt sırasında verdiğiniz e-posta adresine gerekli bilgiler gönderilmiştir. Kaydınızı tamamlamak için e-postanızı kontrol ediniz. ");
        define ("ADDED",                "İçerik başarı ile eklendi.");
        define ("UPDATE_OK",            "Bilgiler güncellendi.");
        define ("MISSING_FIELDS",       "Bilgiler eksik!");
        define ("RESCTRICTED_AREA",     "Yasak Bölge!!");
        define ("ACTIVATE_USER_OK",     "Kullanıcı hesabınız başarıyla etkinleştirildi. Şu andan itibaren kullanabilirsiniz.");
        define ("ACTIVATE_USER_DELETED","Kullanıcı veritabanından <strong>tamamen</strong> kaldırıldı. Bu kullanıcı artık işlem yapamaz.");
        define ("ACTIVATE_USER_ERROR",  "Etkinleştirme işlemi sırasında hata oluştu. Lütfen, daha sonra tekrar deneyin. Hatanın tekrar etmesi durumunda yönetim ile irtibata geçerseniz seviniriz.");
        define ("ACTIVATE_USER_TITLE",  "Kullanıcı Etkinleştirme");
        define ("ACTIVATED_USER",       "Etkinleştirilmiş Hesap !!");
        define ("ACTIVATION_MAIL_HEADER","Merhaba\n\nSiz ya da bir başkası bu e-posta adresini kullanarak {$config['core']['title']} ({$config['core']['url']}) sitesine kayıt yaptırdı.\n    Eğer kaydı siz yaptırdıysanız onaylamak için aşağıdaki bağlantıyı tıklayın.\n\n Onaylamak için tıklayın:");
        define ("ACTIVATION_MAIL_FOOTER","\n İlginiz için teşekkürler.\n Pardus Projesi");
        define ("ACTIVATION_MAIL_TITLE", "{$config['core']['title']} - Aktivasyon");
?>