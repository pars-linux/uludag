-- phpMyAdmin SQL Dump
-- version 2.6.1-rc1
-- http://www.phpmyadmin.net
-- 
-- Sunucu: localhost
-- Çıktı Tarihi: Mart 21, 2005 at 09:43 PM
-- Server sürümü: 4.0.22
-- PHP Sürümü: 5.0.2
-- 
-- Veritabanı: `ugos`
-- 

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `ugo_images`
-- 

DROP TABLE IF EXISTS `ugo_images`;
CREATE TABLE `ugo_images` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `ugo` int(10) unsigned NOT NULL default '0',
  `image` longblob NOT NULL,
  `content_type` varchar(20) NOT NULL default '',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Öneri ile ilgili şemalar' AUTO_INCREMENT=0 ;

-- 
-- Tablo döküm verisi `ugo_images`
-- 


-- --------------------------------------------------------

-- 
-- Tablo yapısı : `ugo_main`
-- 

DROP TABLE IF EXISTS `ugo_main`;
CREATE TABLE `ugo_main` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `sender` int(10) unsigned NOT NULL default '0',
  `title` varchar(100) NOT NULL default '',
  `abstract` text NOT NULL,
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Önerilere ait temel bilgiler' AUTO_INCREMENT=3 ;

-- 
-- Tablo döküm verisi `ugo_main`
-- 

INSERT INTO `ugo_main` (`id`, `sender`, `title`, `abstract`) VALUES (1, 2, 'Pardil: Pardus İyileştirme Listesi', '<a href="http://www.gentoo.org/proj/en/glep/">GLEP</a> (Gentoo Linux Enchancement Proposals) ya da <a href="http://python.org/peps/">PEP</a> (Python Enhancement Proposals) gibi bir sistem kurulması fikri Uludağ listesinde ortaya atılmıştı. Bu uygulama, projeler ile ilgili öneri ve fikirlerin kaybolup gitmemesi için, onları somut, fikir bütünlüğü ve tutarlılık arz eden bir belge olarak saklanılabileceği ve insanların da onları görüntüleyebileceği bir alt yapının gerekliliğini karşılamayı hedeflemektedir.');
INSERT INTO `ugo_main` (`id`, `sender`, `title`, `abstract`) VALUES (2, 1, 'Pardus Proje Yönetimi', 'Bu öneri, Ulusal Dağıtım Projesi ile ilgili bir alt proje başlatılması için gereken şartlar ve izlenmesi gereken prosedür hakkında bilgi vermeyi amaçlamaktadır.');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `ugo_maintainers`
-- 

DROP TABLE IF EXISTS `ugo_maintainers`;
CREATE TABLE `ugo_maintainers` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `ugo` int(10) unsigned NOT NULL default '0',
  `user` int(10) unsigned NOT NULL default '0',
  `timestampB` datetime NOT NULL default '0000-00-00 00:00:00',
  `timestampE` datetime NOT NULL default '9999-12-31 23:59:59',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Öneri bakıcıları' AUTO_INCREMENT=3 ;

-- 
-- Tablo döküm verisi `ugo_maintainers`
-- 

INSERT INTO `ugo_maintainers` (`id`, `ugo`, `user`, `timestampB`, `timestampE`) VALUES (1, 1, 1, '2005-03-11 17:30:00', '9999-12-31 23:59:59');
INSERT INTO `ugo_maintainers` (`id`, `ugo`, `user`, `timestampB`, `timestampE`) VALUES (2, 2, 1, '2005-03-12 02:30:00', '9999-12-31 23:59:59');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `ugo_r_releated`
-- 

DROP TABLE IF EXISTS `ugo_r_releated`;
CREATE TABLE `ugo_r_releated` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `ugo` int(10) unsigned NOT NULL default '0',
  `ugo2` int(10) unsigned NOT NULL default '0',
  `timestampB` datetime NOT NULL default '0000-00-00 00:00:00',
  `timestampE` datetime NOT NULL default '9999-12-31 23:59:59',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Öneri bağımlılıkları' AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `ugo_r_releated`
-- 

INSERT INTO `ugo_r_releated` (`id`, `ugo`, `ugo2`, `timestampB`, `timestampE`) VALUES (1, 2, 1, '2000-01-01 00:00:00', '9999-12-31 23:59:59');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `ugo_r_roles`
-- 

DROP TABLE IF EXISTS `ugo_r_roles`;
CREATE TABLE `ugo_r_roles` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `ugo` int(10) unsigned NOT NULL default '0',
  `user` int(10) unsigned NOT NULL default '0',
  `role` int(10) unsigned NOT NULL default '0',
  `timestampB` datetime NOT NULL default '0000-00-00 00:00:00',
  `timestampE` datetime NOT NULL default '9999-12-31 23:59:59',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='UGO - Rol ilişkileri' AUTO_INCREMENT=2;

-- 
-- Tablo döküm verisi `ugo_r_roles`
-- 

INSERT INTO `ugo_r_roles` (`id`, `ugo`, `user`, `role`, `timestampB`, `timestampE`) VALUES (1, 1, 1, 1, '2005-03-12 00:25:00', '9999-12-31 23:59:59');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `ugo_r_status`
-- 

DROP TABLE IF EXISTS `ugo_r_status`;
CREATE TABLE `ugo_r_status` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `ugo` int(10) unsigned NOT NULL default '0',
  `status` int(10) unsigned NOT NULL default '0',
  `timestampB` datetime NOT NULL default '0000-00-00 00:00:00',
  `timestampE` datetime NOT NULL default '9999-12-31 23:59:59',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Öneri - Durum ilişkileri' AUTO_INCREMENT=4 ;

-- 
-- Tablo döküm verisi `ugo_r_status`
-- 

INSERT INTO `ugo_r_status` (`id`, `ugo`, `status`, `timestampB`, `timestampE`) VALUES (1, 1, 2, '2000-01-01 00:00:00', '9999-12-31 23:59:59');
INSERT INTO `ugo_r_status` (`id`, `ugo`, `status`, `timestampB`, `timestampE`) VALUES (2, 2, 2, '2000-01-01 00:00:00', '9999-12-31 23:59:59');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `ugo_revisions`
-- 

DROP TABLE IF EXISTS `ugo_revisions`;
CREATE TABLE `ugo_revisions` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `ugo` int(10) unsigned NOT NULL default '0',
  `revisor` int(10) unsigned NOT NULL default '0',
  `version` double NOT NULL default '0.1',
  `content` text NOT NULL,
  `notes` text NOT NULL,
  `info` varchar(250) NOT NULL default '',
  `timestamp` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Öneri revizyonları' AUTO_INCREMENT=21 ;

-- 
-- Tablo döküm verisi `ugo_revisions`
-- 

INSERT INTO `ugo_revisions` (`id`, `ugo`, `revisor`, `version`, `content`, `notes`, `info`, `timestamp`) VALUES (3, 1, 1, 1, '<section>\r\n  <title>Problem</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>\r\n<section>\r\n  <title>Kapsam</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>\r\n<section>\r\n  <title>Çözüm</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>', '<note>a</note>\r\n<note>b</note>\r\n<note>c</note>', 'İlk sürüm.', '2005-03-12 02:08:39');
INSERT INTO `ugo_revisions` (`id`, `ugo`, `revisor`, `version`, `content`, `notes`, `info`, `timestamp`) VALUES (20, 2, 1, 1, '<section>\r\n  <title>Prosedür</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>\r\n<section>\r\n  <title>Proje Grupları</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>\r\n<section>\r\n  <title>Şartlar</title>\r\n  <body>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n    <p>...</p>\r\n  </body>\r\n</section>', '...', 'İlk sürüm.', '2000-01-01 00:00:00');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `ugo_roles`
-- 

DROP TABLE IF EXISTS `ugo_roles`;
CREATE TABLE `ugo_roles` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(25) NOT NULL default '',
  `level` tinyint(4) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Roller' AUTO_INCREMENT=4 ;

-- 
-- Tablo döküm verisi `ugo_roles`
-- 

INSERT INTO `ugo_roles` (`id`, `name`, `level`) VALUES (1, 'Proje Yöneticisi', 1);
INSERT INTO `ugo_roles` (`id`, `name`, `level`) VALUES (2, 'Geliştirici', 2);
INSERT INTO `ugo_roles` (`id`, `name`, `level`) VALUES (3, 'Destekçi', 3);

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `ugo_status`
-- 

DROP TABLE IF EXISTS `ugo_status`;
CREATE TABLE `ugo_status` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(25) NOT NULL default '',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM COMMENT='Öneri durumları' AUTO_INCREMENT=4 ;

-- 
-- Tablo döküm verisi `ugo_status`
-- 

INSERT INTO `ugo_status` (`id`, `name`) VALUES (1, 'Onay Bekliyor');
INSERT INTO `ugo_status` (`id`, `name`) VALUES (2, 'Aktif');
INSERT INTO `ugo_status` (`id`, `name`) VALUES (3, 'Askıda');

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
) TYPE=MyISAM AUTO_INCREMENT=4 ;

-- 
-- Tablo döküm verisi `users`
-- 

INSERT INTO `users` (`id`, `username`, `password`, `email`, `name`, `level`) VALUES (1, 'admin', '21232f297a57a5a743894a0e4a801fc3', 'ugos@uludag.org.tr', 'Pardil Admin', 0);
