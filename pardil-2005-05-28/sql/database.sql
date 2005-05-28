-- phpMyAdmin SQL Dump
-- version 2.6.1-rc1
-- http://www.phpmyadmin.net
-- 
-- Sunucu: localhost
-- Çıktı Tarihi: Mart 21, 2005 at 10:29 PM
-- Server sürümü: 4.0.22
-- PHP Sürümü: 5.0.2
-- 
-- Veritabanı: `pardil`
-- 

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardil_images`
-- 

DROP TABLE IF EXISTS `pardil_images`;
CREATE TABLE `pardil_images` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `proposal` int(10) unsigned NOT NULL default '0',
  `image` longblob NOT NULL,
  `content_type` varchar(20) NOT NULL default '',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Öneri ile ilgili şemalar' AUTO_INCREMENT=1 ;

-- 
-- Tablo döküm verisi `pardil_images`
-- 


-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardil_main`
-- 

DROP TABLE IF EXISTS `pardil_main`;
CREATE TABLE `pardil_main` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `sender` int(10) unsigned NOT NULL default '0',
  `title` varchar(100) NOT NULL default '',
  `abstract` text NOT NULL,
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Önerilere ait temel bilgiler' AUTO_INCREMENT=3 ;

-- 
-- Tablo döküm verisi `pardil_main`
-- 

INSERT INTO `pardil_main` (`id`, `sender`, `title`, `abstract`) VALUES (1, 1, 'Pardil: Pardus İyileştirme Listesi', '<a href="http://www.gentoo.org/proj/en/glep/">GLEP</a> (Gentoo Linux Enchancement Proposals) ya da <a href="http://python.org/peps/">PEP</a> (Python Enhancement Proposals) gibi bir sistem kurulması fikri Uludağ listesinde ortaya atılmıştı. Bu uygulama, projeler ile ilgili öneri ve fikirlerin kaybolup gitmemesi için, onları somut, fikir bütünlüğü ve tutarlılık arz eden bir belge olarak saklanılabileceği ve insanların da onları görüntüleyebileceği bir alt yapının gerekliliğini karşılamayı hedeflemektedir.');
INSERT INTO `pardil_main` (`id`, `sender`, `title`, `abstract`) VALUES (2, 1, 'Pardus Proje Yönetimi', 'Bu öneri, Ulusal Dağıtım Projesi ile ilgili bir alt proje başlatılması için gereken şartlar ve izlenmesi gereken prosedür hakkında bilgi vermeyi amaçlamaktadır.');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardil_maintainers`
-- 

DROP TABLE IF EXISTS `pardil_maintainers`;
CREATE TABLE `pardil_maintainers` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `proposal` int(10) unsigned NOT NULL default '0',
  `user` int(10) unsigned NOT NULL default '0',
  `timestampB` datetime NOT NULL default '0000-00-00 00:00:00',
  `timestampE` datetime NOT NULL default '9999-12-31 23:59:59',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Öneri bakıcıları' AUTO_INCREMENT=3 ;

-- 
-- Tablo döküm verisi `pardil_maintainers`
-- 

INSERT INTO `pardil_maintainers` (`id`, `proposal`, `user`, `timestampB`, `timestampE`) VALUES (1, 1, 1, '2005-03-11 17:00:00', '9990-12-31 23:59:59');
INSERT INTO `pardil_maintainers` (`id`, `proposal`, `user`, `timestampB`, `timestampE`) VALUES (2, 2, 1, '2005-03-11 17:30:00', '9999-12-31 23:59:59');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardil_r_releated`
-- 

DROP TABLE IF EXISTS `pardil_r_releated`;
CREATE TABLE `pardil_r_releated` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `proposal` int(10) unsigned NOT NULL default '0',
  `proposal2` int(10) unsigned NOT NULL default '0',
  `timestampB` datetime NOT NULL default '0000-00-00 00:00:00',
  `timestampE` datetime NOT NULL default '9999-12-31 23:59:59',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Öneri bağımlılıkları' AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `pardil_r_releated`
-- 

INSERT INTO `pardil_r_releated` (`id`, `proposal`, `proposal2`, `timestampB`, `timestampE`) VALUES (1, 2, 1, '2000-01-01 00:00:00', '9999-12-31 23:59:59');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardil_r_roles`
-- 

DROP TABLE IF EXISTS `pardil_r_roles`;
CREATE TABLE `pardil_r_roles` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `proposal` int(10) unsigned NOT NULL default '0',
  `user` int(10) unsigned NOT NULL default '0',
  `role` int(10) unsigned NOT NULL default '0',
  `timestampB` datetime NOT NULL default '0000-00-00 00:00:00',
  `timestampE` datetime NOT NULL default '9999-12-31 23:59:59',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='UGO - Rol ilişkileri' AUTO_INCREMENT=1 ;

-- 
-- Tablo döküm verisi `pardil_r_roles`
-- 


-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardil_r_status`
-- 

DROP TABLE IF EXISTS `pardil_r_status`;
CREATE TABLE `pardil_r_status` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `proposal` int(10) unsigned NOT NULL default '0',
  `status` int(10) unsigned NOT NULL default '0',
  `timestampB` datetime NOT NULL default '0000-00-00 00:00:00',
  `timestampE` datetime NOT NULL default '9999-12-31 23:59:59',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Öneri - Durum ilişkileri' AUTO_INCREMENT=3 ;

-- 
-- Tablo döküm verisi `pardil_r_status`
-- 

INSERT INTO `pardil_r_status` (`id`, `proposal`, `status`, `timestampB`, `timestampE`) VALUES (1, 1, 2, '2000-01-01 00:00:00', '9999-12-31 23:59:59');
INSERT INTO `pardil_r_status` (`id`, `proposal`, `status`, `timestampB`, `timestampE`) VALUES (2, 2, 2, '2000-01-01 00:00:00', '9999-12-31 23:59:59');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardil_revisions`
-- 

DROP TABLE IF EXISTS `pardil_revisions`;
CREATE TABLE `pardil_revisions` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `proposal` int(10) unsigned NOT NULL default '0',
  `revisor` int(10) unsigned NOT NULL default '0',
  `version` double NOT NULL default '0.1',
  `content` text NOT NULL,
  `info` varchar(250) NOT NULL default '',
  `timestamp` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Öneri revizyonları' AUTO_INCREMENT=21 ;

-- 
-- Tablo döküm verisi `pardil_revisions`
-- 

INSERT INTO `pardil_revisions` (`id`, `proposal`, `revisor`, `version`, `content`, `info`, `timestamp`) VALUES (3, 1, 1, 1, '<section>\r\n  <title>Problem</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>\r\n<section>\r\n  <title>Kapsam</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>\r\n<section>\r\n  <title>Çözüm</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>', 'İlk sürüm.', '2005-03-12 02:08:39');
INSERT INTO `pardil_revisions` (`id`, `proposal`, `revisor`, `version`, `content`, `info`, `timestamp`) VALUES (20, 2, 1, 1, '<section>\r\n  <title>Prosedür</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>\r\n<section>\r\n  <title>Proje Grupları</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>\r\n<section>\r\n  <title>Şartlar</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>', 'İlk sürüm.', '2000-01-01 00:00:00');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardil_roles`
-- 

DROP TABLE IF EXISTS `pardil_roles`;
CREATE TABLE `pardil_roles` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(25) NOT NULL default '',
  `level` tinyint(4) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Roller' AUTO_INCREMENT=4 ;

-- 
-- Tablo döküm verisi `pardil_roles`
-- 

INSERT INTO `pardil_roles` (`id`, `name`, `level`) VALUES (1, 'Project Manager', 1);
INSERT INTO `pardil_roles` (`id`, `name`, `level`) VALUES (2, 'Developer', 2);
INSERT INTO `pardil_roles` (`id`, `name`, `level`) VALUES (3, 'Contributor', 3);

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardil_status`
-- 

DROP TABLE IF EXISTS `pardil_status`;
CREATE TABLE `pardil_status` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(25) NOT NULL default '',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Öneri durumları' AUTO_INCREMENT=4 ;

-- 
-- Tablo döküm verisi `pardil_status`
-- 

INSERT INTO `pardil_status` (`id`, `name`) VALUES (1, 'Pending');
INSERT INTO `pardil_status` (`id`, `name`) VALUES (2, 'Active');
INSERT INTO `pardil_status` (`id`, `name`) VALUES (3, 'Locked');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `users`
-- 

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `username` varchar(25) NOT NULL default '',
  `password` varchar(32) NOT NULL default '',
  `email` varchar(50) NOT NULL default '',
  `name` varchar(60) NOT NULL default '',
  `level` tinyint(4) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `users`
-- 

INSERT INTO `users` (`id`, `username`, `password`, `email`, `name`, `level`) VALUES (1, 'admin', '21232f297a57a5a743894a0e4a801fc3', 'ugos@uludag.org.tr', 'Pardil Admin', 0);


-- 
-- Tablo yapısı : `sessions`
-- 

CREATE TABLE `sessions` (
  `id` varchar(32) NOT NULL default '',
  `user` int(10) unsigned NOT NULL default '0',
  `timestamp` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Oturum bilgileri' AUTO_INCREMENT=1;

-- 
-- Tablo yapısı : `options`
-- 

CREATE TABLE `options` (
  `opt` varchar(40) NOT NULL default '',
  `value` tinytext NOT NULL,
  `comment` tinytext NOT NULL,
  PRIMARY KEY  (`opt`),
  FULLTEXT KEY `option` (`opt`)
) TYPE=MyISAM COMMENT='Seçenekler';

-- 
-- Tablo döküm verisi `options`
-- 

INSERT INTO `options` (`opt`, `value`, `comment`) VALUES ('level_proposal_new_approved', '10', 'Önerinin otomatik olarak onaylanması için gereken en düşük kullanıcı seviyesi.');
INSERT INTO `options` (`opt`, `value`, `comment`) VALUES ('level_proposal_new', '200', 'Öneri eklemek için gereken en düşük kullanıcı seviyesi.');
INSERT INTO `options` (`opt`, `value`, `comment`) VALUES ('register_activation_required', 'true', 'Kayıt sonrası aktivasyon gerekliliği.');
INSERT INTO `options` (`opt`, `value`, `comment`) VALUES ('site_name', 'Pardil', 'Site adı');
INSERT INTO `options` (`opt`, `value`, `comment`) VALUES ('site_title', 'Pardus İyileştirme Listesi', 'Site başlığı');
INSERT INTO `options` (`opt`, `value`, `comment`) VALUES ('site_url', 'http://sinus.homelinus.org/pardil/', 'Site adresi');
INSERT INTO `options` (`opt`, `value`, `comment`) VALUES ('temp_password_timeout', '900', 'Geçici şifre ömrü (saniye cinsinden)');
INSERT INTO `options` (`opt`, `value`, `comment`) VALUES ('session_timeout', '900', 'Oturum ömrü (saniye cinsinden)');
INSERT INTO `options` (`opt`, `value`, `comment`) VALUES ('addresschange_activation_required', 'true', '');
INSERT INTO `options` (`opt`, `value`, `comment`) VALUES ('level_proposal_edit', '10', 'Önerileri bakıcı olmadan değitştirebilmek için gereken en düşük kullanıcı seviyesi.');
INSERT INTO `options` (`opt`, `value`, `comment`) VALUES ('min_username_length', '5', 'En kısa kullanıcı ismi uzunluğu.');
INSERT INTO `options` (`opt`, `value`, `comment`) VALUES ('min_password_length', '6', 'En kısa şifre uzunluğu.');

-- 
-- Tablo yapısı : `activation`
-- 

CREATE TABLE `activation` (
  `user` int(10) unsigned NOT NULL default '0',
  `code` varchar(32) NOT NULL default '',
  `status` tinyint(1) NOT NULL default '0',
  `timestamp` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`user`)
) TYPE=MyISAM COMMENT='Aktivasyon kodları' AUTO_INCREMENT=2;

-- 
-- Tablo döküm verisi `activation`
-- 

INSERT INTO `activation` (`user`, `code`, `status`) VALUES (1, 'c4ca4238a0b923820dcc509a6f75849b', 1);


-- 
-- Tablo yapısı : `temp_passwords`
-- 

CREATE TABLE `temp_passwords` (
  `user` int(10) unsigned NOT NULL default '0',
  `password` varchar(10) NOT NULL default '',
  `timestamp` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`user`)
) TYPE=MyISAM COMMENT='Geçici şifreler';


-- 
-- Tablo yapısı : `floodcontrol`
-- 

CREATE TABLE `floodcontrol` (
  `no` int(10) unsigned NOT NULL auto_increment,
  `label` varchar(25) NOT NULL default '',
  `ip` varchar(15) NOT NULL default '',
  `timestamp` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`no`)
) TYPE=MyISAM COMMENT='Olası saldırıları engellemek için kullanılacak kütük' AUTO_INCREMENT=1 ;
