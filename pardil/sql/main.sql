-- phpMyAdmin SQL Dump
-- version 2.6.2-pl1
-- http://www.phpmyadmin.net
-- 
-- Sunucu: localhost
-- Çıktı Tarihi: Ağustos 09, 2005 at 08:31 PM
-- Server sürümü: 4.1.12
-- PHP Sürümü: 5.0.4
-- 
-- Veritabanı: `pardil_py`
-- 

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `groups`
-- 

CREATE TABLE groups (
  gid int(10) unsigned NOT NULL auto_increment,
  label varchar(32) collate utf8_turkish_ci NOT NULL default '',
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  timeE datetime NOT NULL default '9999-12-31 00:00:00',
  PRIMARY KEY  (gid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=4 ;

-- 
-- Tablo döküm verisi `groups`
-- 

INSERT INTO groups (gid, label, timeB, timeE) VALUES (1, 'Geliştiriciler', '0000-00-00 00:00:00', '9999-12-31 00:00:00');
INSERT INTO groups (gid, label, timeB, timeE) VALUES (2, 'Katkıcılar', '0000-00-00 00:00:00', '9999-12-31 00:00:00');
INSERT INTO groups (gid, label, timeB, timeE) VALUES (3, 'Editörler', '0000-00-00 00:00:00', '9999-12-31 00:00:00');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `proposals`
-- 

CREATE TABLE proposals (
  pid int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  startup datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (pid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `proposals`
-- 

INSERT INTO proposals (pid, uid, startup) VALUES (1, 0, '2005-07-31 18:33:00');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `proposals_versions`
-- 

CREATE TABLE proposals_versions (
  vid int(10) unsigned NOT NULL auto_increment,
  pid int(10) unsigned NOT NULL default '0',
  version varchar(16) collate utf8_turkish_ci NOT NULL default '0',
  title varchar(100) collate utf8_turkish_ci NOT NULL default '',
  content text collate utf8_turkish_ci NOT NULL,
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  changelog tinytext collate utf8_turkish_ci NOT NULL,
  PRIMARY KEY  (vid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=3 ;

-- 
-- Tablo döküm verisi `proposals_versions`
-- 

INSERT INTO proposals_versions (vid, pid, version, title, content, timeB, changelog) VALUES (1, 1, '1.0', 'Öneri Takip Sistemi', 'Problem\r\n========\r\n\r\n...\r\n\r\nÇözüm\r\n=======\r\n\r\n...\r\n\r\nKapsam\r\n=======\r\n\r\n...', '2005-08-07 15:00:00', '');
INSERT INTO proposals_versions (vid, pid, version, title, content, timeB, changelog) VALUES (2, 1, '1.1', 'Öneri Takip Sistemi', 'Problem\r\n========\r\n\r\n...\r\n\r\nÇözüm\r\n=======\r\n\r\n...\r\n\r\nKapsam\r\n=======\r\n\r\n...', '2005-08-07 15:00:00', 'Yazım hataları düzeltildi.');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `rel_groups`
-- 

CREATE TABLE rel_groups (
  relid int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  gid int(10) unsigned NOT NULL default '0',
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  timeE datetime NOT NULL default '9999-12-31 00:00:00',
  PRIMARY KEY  (relid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=3 ;

-- 
-- Tablo döküm verisi `rel_groups`
-- 

INSERT INTO rel_groups (relid, uid, gid, timeB, timeE) VALUES (1, 1, 1, '0000-00-00 00:00:00', '9999-12-31 00:00:00');
INSERT INTO rel_groups (relid, uid, gid, timeB, timeE) VALUES (2, 1, 2, '0000-00-00 00:00:00', '9999-12-31 00:00:00');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `rel_maintainers`
-- 

CREATE TABLE rel_maintainers (
  relid int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  pid int(10) unsigned NOT NULL default '0',
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  timeE datetime NOT NULL default '9999-12-31 00:00:00',
  PRIMARY KEY  (relid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=3 ;

-- 
-- Tablo döküm verisi `rel_maintainers`
-- 

INSERT INTO rel_maintainers (relid, uid, pid, timeB, timeE) VALUES (1, 1, 1, '0000-00-00 00:00:00', '9999-12-31 00:00:00');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `rel_rights`
-- 

CREATE TABLE rel_rights (
  relid int(10) unsigned NOT NULL auto_increment,
  rid int(10) unsigned NOT NULL default '0',
  gid int(10) unsigned NOT NULL default '0',
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  timeE datetime NOT NULL default '9999-12-31 00:00:00',
  PRIMARY KEY  (relid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `rel_rights`
-- 

INSERT INTO rel_rights (relid, rid, gid, timeB, timeE) VALUES (1, 1, 1, '0000-00-00 00:00:00', '9999-12-31 00:00:00');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `rights`
-- 

CREATE TABLE rights (
  rid int(10) unsigned NOT NULL auto_increment,
  keyword varchar(32) collate utf8_turkish_ci NOT NULL default '',
  label varchar(100) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (rid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `rights`
-- 

INSERT INTO rights (rid, keyword, label) VALUES (1, 'proposals_add', 'Öneri Ekleme');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `users`
-- 

CREATE TABLE users (
  uid int(10) unsigned NOT NULL auto_increment,
  sid varchar(32) collate utf8_turkish_ci NOT NULL default '',
  username varchar(32) collate utf8_turkish_ci NOT NULL default '',
  `password` varchar(32) collate utf8_turkish_ci NOT NULL default '',
  email varchar(64) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (uid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci PACK_KEYS=0 AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `users`
-- 

INSERT INTO users (uid, sid, username, password, email) VALUES (1, '', 'bahadir', '9acbbafe2b77d2bae46a3348065967f0', 'bahadir@haftalik.net');
