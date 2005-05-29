-- phpMyAdmin SQL Dump
-- version 2.6.2-pl1
-- http://www.phpmyadmin.net
-- 
-- Sunucu: localhost
-- Çıktı Tarihi: Mayıs 29, 2005 at 09:23 PM
-- Server sürümü: 4.1.12
-- PHP Sürümü: 5.0.3
-- 
-- Veritabanı: `pardil`
-- 

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `activation`
-- 

CREATE TABLE activation (
  `user` int(10) unsigned NOT NULL default '0',
  code varchar(32) collate utf8_turkish_ci NOT NULL default '',
  `status` tinyint(1) NOT NULL default '0',
  `timestamp` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`user`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Aktivasyon kodları ve kullanıcıların aktivasyon durumları';

-- 
-- Tablo döküm verisi `activation`
-- 

INSERT INTO activation (user, code, status, timestamp) VALUES (1, 'c4ca4238a0b923820dcc509a6f75849b', 1, '0000-00-00 00:00:00');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `flood_control`
-- 

CREATE TABLE flood_control (
  `no` int(10) unsigned NOT NULL auto_increment,
  label varchar(25) collate utf8_turkish_ci NOT NULL default '',
  ip varchar(15) collate utf8_turkish_ci NOT NULL default '',
  `timestamp` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`no`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Olası bot saldırılarını engellemek için kullanılacak ' AUTO_INCREMENT=1 ;

-- 
-- Tablo döküm verisi `flood_control`
-- 


-- --------------------------------------------------------

-- 
-- Tablo yapısı : `lst_proposal_status`
-- 

CREATE TABLE lst_proposal_status (
  id int(10) unsigned NOT NULL auto_increment,
  name varchar(25) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Öneri durumları' AUTO_INCREMENT=4 ;

-- 
-- Tablo döküm verisi `lst_proposal_status`
-- 

INSERT INTO lst_proposal_status (id, name) VALUES (1, 'Beklemede');
INSERT INTO lst_proposal_status (id, name) VALUES (2, 'Aktif');
INSERT INTO lst_proposal_status (id, name) VALUES (3, 'Kilitli');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `lst_user_roles`
-- 

CREATE TABLE lst_user_roles (
  id int(10) unsigned NOT NULL auto_increment,
  name varchar(25) collate utf8_turkish_ci NOT NULL default '',
  `level` tinyint(4) NOT NULL default '0',
  PRIMARY KEY  (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Kullanıcı rolleri' AUTO_INCREMENT=4 ;

-- 
-- Tablo döküm verisi `lst_user_roles`
-- 

INSERT INTO lst_user_roles (id, name, level) VALUES (1, 'Proje Yöneticisi', 1);
INSERT INTO lst_user_roles (id, name, level) VALUES (2, 'Geliştirici', 2);
INSERT INTO lst_user_roles (id, name, level) VALUES (3, 'Katkıcı', 3);

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `options`
-- 

CREATE TABLE options (
  opt varchar(40) collate utf8_turkish_ci NOT NULL default '',
  `value` tinytext collate utf8_turkish_ci NOT NULL,
  `comment` tinytext collate utf8_turkish_ci NOT NULL,
  PRIMARY KEY  (opt),
  FULLTEXT KEY `option` (opt)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Seçenekler';

-- 
-- Tablo döküm verisi `options`
-- 

INSERT INTO options (opt, value, comment) VALUES ('level_proposal_new_approved', '10', 'Önerinin otomatik olarak onaylanması için gereken en düşük kullanıcı seviyesi.');
INSERT INTO options (opt, value, comment) VALUES ('level_proposal_new', '200', 'Öneri eklemek için gereken en düşük kullanıcı seviyesi.');
INSERT INTO options (opt, value, comment) VALUES ('register_activation_required', 'true', 'Kayıt sonrası aktivasyon gerekliliği.');
INSERT INTO options (opt, value, comment) VALUES ('site_name', 'Pardil', 'Site adı');
INSERT INTO options (opt, value, comment) VALUES ('site_title', 'Pardus İyileştirme Listesi', 'Site başlığı');
INSERT INTO options (opt, value, comment) VALUES ('site_url', 'http://pardil/', 'Site adresi');
INSERT INTO options (opt, value, comment) VALUES ('temp_password_timeout', '900', 'Geçici şifre ömrü (saniye cinsinden)');
INSERT INTO options (opt, value, comment) VALUES ('session_timeout', '900', 'Oturum ömrü (saniye cinsinden)');
INSERT INTO options (opt, value, comment) VALUES ('addresschange_activation_required', 'true', '');
INSERT INTO options (opt, value, comment) VALUES ('level_proposal_edit', '10', 'Önerileri bakıcı olmadan değitştirebilmek için gereken en düşük kullanıcı seviyesi.');
INSERT INTO options (opt, value, comment) VALUES ('min_username_length', '5', 'En kısa kullanıcı ismi uzunluğu.');
INSERT INTO options (opt, value, comment) VALUES ('min_password_length', '6', 'En kısa şifre uzunluğu.');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `proposal_attachments`
-- 

CREATE TABLE proposal_attachments (
  id int(10) unsigned NOT NULL auto_increment,
  proposal int(10) unsigned NOT NULL default '0',
  content longblob NOT NULL,
  content_type varchar(20) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Önerilere iliştirilen eklentiler.' AUTO_INCREMENT=1 ;

-- 
-- Tablo döküm verisi `proposal_attachments`
-- 


-- --------------------------------------------------------

-- 
-- Tablo yapısı : `proposal_main`
-- 

CREATE TABLE proposal_main (
  id int(10) unsigned NOT NULL auto_increment,
  sender int(10) unsigned NOT NULL default '0',
  title varchar(100) collate utf8_turkish_ci NOT NULL default '',
  abstract text collate utf8_turkish_ci NOT NULL,
  PRIMARY KEY  (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Önerilere ait temel bilgiler' AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `proposal_main`
-- 

INSERT INTO proposal_main (id, sender, title, abstract) VALUES (1, 1, 'Pardil: Pardus İyileştirme Listesi', '<a href="http://www.gentoo.org/proj/en/glep/">GLEP</a> (Gentoo Linux Enchancement Proposals) ya da <a href="http://python.org/peps/">PEP</a> (Python Enhancement Proposals) gibi bir sistem kurulması fikri Uludağ listesinde ortaya atılmıştı. Bu uygulama, projeler ile ilgili öneri ve fikirlerin kaybolup gitmemesi için, onları somut, fikir bütünlüğü ve tutarlılık arz eden bir belge olarak saklanılabileceği ve insanların da onları görüntüleyebileceği bir alt yapının gerekliliğini karşılamayı hedeflemektedir.');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `proposal_maintainers`
-- 

CREATE TABLE proposal_maintainers (
  id int(10) unsigned NOT NULL auto_increment,
  proposal int(10) unsigned NOT NULL default '0',
  `user` int(10) unsigned NOT NULL default '0',
  timestampB datetime NOT NULL default '0000-00-00 00:00:00',
  timestampE datetime NOT NULL default '9999-12-31 23:59:59',
  PRIMARY KEY  (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Öneri sorumluları' AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `proposal_maintainers`
-- 

INSERT INTO proposal_maintainers (id, proposal, user, timestampB, timestampE) VALUES (1, 1, 1, '2005-03-11 17:00:00', '9990-12-31 23:59:59');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `proposal_revisions`
-- 

CREATE TABLE proposal_revisions (
  id int(10) unsigned NOT NULL auto_increment,
  proposal int(10) unsigned NOT NULL default '0',
  revisor int(10) unsigned NOT NULL default '0',
  version double NOT NULL default '0.1',
  content text collate utf8_turkish_ci NOT NULL,
  info varchar(250) collate utf8_turkish_ci NOT NULL default '',
  `timestamp` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Öneri revizyonları' AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `proposal_revisions`
-- 

INSERT INTO proposal_revisions (id, proposal, revisor, version, content, info, timestamp) VALUES (1, 1, 1, 1, '<section>\r\n  <title>Problem</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>\r\n<section>\r\n  <title>Kapsam</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>\r\n<section>\r\n  <title>Çözüm</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>', 'İlk sürüm.', '2005-03-12 02:08:39');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `r_releated_proposals`
-- 

CREATE TABLE r_releated_proposals (
  id int(10) unsigned NOT NULL auto_increment,
  proposal int(10) unsigned NOT NULL default '0',
  proposal2 int(10) unsigned NOT NULL default '0',
  timestampB datetime NOT NULL default '0000-00-00 00:00:00',
  timestampE datetime NOT NULL default '9999-12-31 23:59:59',
  PRIMARY KEY  (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Birbiriyle ilgili önerilerin listesi' AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `r_releated_proposals`
-- 

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `r_roles_proposals`
-- 

CREATE TABLE r_roles_proposals (
  id int(10) unsigned NOT NULL auto_increment,
  proposal int(10) unsigned NOT NULL default '0',
  `user` int(10) unsigned NOT NULL default '0',
  role int(10) unsigned NOT NULL default '0',
  timestampB datetime NOT NULL default '0000-00-00 00:00:00',
  timestampE datetime NOT NULL default '9999-12-31 23:59:59',
  PRIMARY KEY  (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Öneriler, kullanıcılar ve roller arasındaki ilişki.' AUTO_INCREMENT=1 ;

-- 
-- Tablo döküm verisi `r_roles_proposals`
-- 


-- --------------------------------------------------------

-- 
-- Tablo yapısı : `r_status_proposal`
-- 

CREATE TABLE r_status_proposal (
  id int(10) unsigned NOT NULL auto_increment,
  proposal int(10) unsigned NOT NULL default '0',
  `status` int(10) unsigned NOT NULL default '0',
  timestampB datetime NOT NULL default '0000-00-00 00:00:00',
  timestampE datetime NOT NULL default '9999-12-31 23:59:59',
  PRIMARY KEY  (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Öneri - Durum ilişkileri' AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `r_status_proposal`
-- 

INSERT INTO r_status_proposal (id, proposal, status, timestampB, timestampE) VALUES (1, 1, 2, '2000-01-01 00:00:00', '9999-12-31 23:59:59');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `sessions`
-- 

CREATE TABLE sessions (
  id varchar(32) collate utf8_turkish_ci NOT NULL default '',
  `user` int(10) unsigned NOT NULL default '0',
  `timestamp` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Oturum bilgileri';

-- 
-- Tablo döküm verisi `sessions`
-- 


-- --------------------------------------------------------

-- 
-- Tablo yapısı : `temp_passwords`
-- 

CREATE TABLE temp_passwords (
  `user` int(10) unsigned NOT NULL default '0',
  `password` varchar(10) collate utf8_turkish_ci NOT NULL default '',
  `timestamp` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`user`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Geçici şifreler';

-- 
-- Tablo döküm verisi `temp_passwords`
-- 


-- --------------------------------------------------------

-- 
-- Tablo yapısı : `users`
-- 

CREATE TABLE users (
  id int(10) unsigned NOT NULL auto_increment,
  username varchar(25) collate utf8_turkish_ci NOT NULL default '',
  `password` varchar(32) collate utf8_turkish_ci NOT NULL default '',
  email varchar(50) collate utf8_turkish_ci NOT NULL default '',
  name varchar(60) collate utf8_turkish_ci NOT NULL default '',
  `level` tinyint(4) NOT NULL default '0',
  PRIMARY KEY  (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `users`
-- 

INSERT INTO users (id, username, password, email, name, level) VALUES (1, 'admin', '21232f297a57a5a743894a0e4a801fc3', 'pardil-admin@uludag.org.tr', 'Pardil Admin', 0);

-- 
-- Tablo yapısı : `proposal_comments`
-- 

CREATE TABLE `proposal_comments` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `proposal` int(10) unsigned NOT NULL default '0',
  `user` int(10) unsigned NOT NULL default '0',
  `comment` text collate utf8_turkish_ci NOT NULL,
   PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Önerilere iliştirilen yorumlar.' AUTO_INCREMENT=1 ;
                  
