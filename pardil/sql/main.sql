-- phpMyAdmin SQL Dump
-- version 2.6.2-pl1
-- http://www.phpmyadmin.net
-- 
-- Sunucu: localhost
-- Çıktı Tarihi: Ağustos 06, 2005 at 01:56 PM
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
  startup datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (pid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=1;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `proposals_versions`
-- 

CREATE TABLE proposals_versions (
  vid int(10) unsigned NOT NULL auto_increment,
  pid int(10) unsigned NOT NULL default '0',
  version float NOT NULL default '0',
  title varchar(100) collate utf8_turkish_ci NOT NULL default '',
  content text collate utf8_turkish_ci NOT NULL,
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (vid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `rel_groups`
-- 

CREATE TABLE rel_groups (
  rid int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  gid int(10) unsigned NOT NULL default '0',
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  timeE datetime NOT NULL default '9999-12-31 00:00:00',
  PRIMARY KEY  (rid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=1 ;

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
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci PACK_KEYS=0 AUTO_INCREMENT=1 ;
