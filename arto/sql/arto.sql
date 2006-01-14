-- phpMyAdmin SQL Dump
-- version 2.6.4 - Pardus v1.0
-- http://www.phpmyadmin.net
-- 
-- Sunucu: localhost
-- Çıktı Tarihi: Ocak 14, 2006 at 09:53 PM
-- Server sürümü: 4.1.14
-- PHP Sürümü: 5.1.1
-- 
-- Veritabanı: `arto`
-- 

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `arto_comments`
-- 

CREATE TABLE `arto_comments` (
  `id` int(11) NOT NULL auto_increment,
  `fid` int(11) NOT NULL default '0',
  `uid` int(11) NOT NULL default '0',
  `date` tinytext character set utf8 collate utf8_turkish_ci NOT NULL,
  `comment` text character set utf8 collate utf8_turkish_ci NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- 
-- Tablo döküm verisi `arto_comments`
-- 


-- --------------------------------------------------------

-- 
-- Tablo yapısı : `arto_files`
-- 

CREATE TABLE `arto_files` (
  `id` int(11) NOT NULL auto_increment,
  `type` int(11) NOT NULL default '0',
  `sub_type` int(11) NOT NULL default '0',
  `name` varchar(200) character set utf8 collate utf8_turkish_ci NOT NULL default '',
  `license` int(11) NOT NULL default '0',
  `user` int(11) NOT NULL default '0',
  `supervisor` int(11) default '0',
  `path` varchar(255) character set utf8 collate utf8_turkish_ci NOT NULL default '',
  `desc` text character set utf8 collate utf8_turkish_ci,
  `note` varchar(255) character set utf8 collate utf8_turkish_ci default NULL,
  `rate` set('0','1','2','3','4','5') character set utf8 collate utf8_turkish_ci NOT NULL default '0',
  `state` set('0','1') character set utf8 collate utf8_turkish_ci NOT NULL default '0',
  `counter` int(11) NOT NULL default '0',
  `release` tinytext character set utf8 collate utf8_turkish_ci NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='All about files' AUTO_INCREMENT=1 ;

-- 
-- Tablo döküm verisi `arto_files`
-- 


-- --------------------------------------------------------

-- 
-- Tablo yapısı : `arto_license`
-- 

CREATE TABLE `arto_license` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(200) character set utf8 collate utf8_turkish_ci NOT NULL default '',
  `link` varchar(255) character set utf8 collate utf8_turkish_ci NOT NULL default '',
  `description` varchar(255) character set utf8 collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='All about licenses' AUTO_INCREMENT=3 ;

-- 
-- Tablo döküm verisi `arto_license`
-- 

INSERT INTO `arto_license` VALUES (1, 'CC Attribution-ShareAlike', 'http://creativecommons.org/licenses/by-sa/2.0/', 'Share Alike. If you alter, transform, or build upon this work, you may distribute the resulting work only under a license identical to this one.');
INSERT INTO `arto_license` VALUES (2, 'GNU General Public License', 'http://creativecommons.org/licenses/GPL/2.0/', 'The GNU General Public License is a Free Software license. Like any Free Software license, it grants to you the four following freedoms:\r\n\r\n   0. The freedom to run the program for any purpose.\r\n   1. The freedom to study how the program works and adapt i');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `arto_types`
-- 

CREATE TABLE `arto_types` (
  `id` int(11) NOT NULL auto_increment,
  `type` varchar(200) character set utf8 collate utf8_turkish_ci NOT NULL default '',
  `parent_id` int(11) NOT NULL default '0',
  `admin` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Theme types' AUTO_INCREMENT=9 ;

-- 
-- Tablo döküm verisi `arto_types`
-- 

INSERT INTO `arto_types` VALUES (1, 'Duvar Kağıdı', 0, 0);
INSERT INTO `arto_types` VALUES (2, 'Temalar', 0, 0);
INSERT INTO `arto_types` VALUES (3, 'Pardus', 1, 0);
INSERT INTO `arto_types` VALUES (4, 'KDE', 1, 0);
INSERT INTO `arto_types` VALUES (5, 'KDE', 2, 0);
INSERT INTO `arto_types` VALUES (6, 'amaroK', 2, 0);
INSERT INTO `arto_types` VALUES (7, 'Kopete', 2, 0);
INSERT INTO `arto_types` VALUES (8, 'Ekran Görüntüleri', 1, 0);

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `arto_users`
-- 

CREATE TABLE `arto_users` (
  `id` int(11) NOT NULL auto_increment,
  `uname` varchar(30) character set utf8 collate utf8_turkish_ci NOT NULL default '',
  `password` varchar(30) character set utf8 collate utf8_turkish_ci NOT NULL default '',
  `name` varchar(120) character set utf8 collate utf8_turkish_ci NOT NULL default '',
  `email` varchar(200) character set utf8 collate utf8_turkish_ci NOT NULL default '',
  `web` varchar(200) character set utf8 collate utf8_turkish_ci default NULL,
  `state` set('0','1','2','3') character set utf8 collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='All about users' AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `arto_users`
-- 

INSERT INTO `arto_users` VALUES (1, 'pardusman', 'pardus', 'PardusMan', 'arto@uludag.org.tr', 'http://sanat.uludag.org.tr', '0');
