-- phpMyAdmin SQL Dump
-- version 2.6.4 - Pardus v1.0
-- http://www.phpmyadmin.net
-- 
-- Sunucu: localhost
-- Çıktı Tarihi: Ocak 19, 2006 at 21:50 PM
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
  `date` tinytext NOT NULL,
  `comment` text NOT NULL,
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `arto_files`
-- 

CREATE TABLE `arto_files` (
  `id` int(11) NOT NULL auto_increment,
  `type` int(11) NOT NULL default '0',
  `sub_type` int(11) NOT NULL default '0',
  `name` varchar(200) NOT NULL default '',
  `license` int(11) NOT NULL default '0',
  `user` int(11) NOT NULL default '0',
  `supervisor` int(11) default '0',
  `path` varchar(255) NOT NULL default '',
  `description` text,
  `note` varchar(255) default NULL,
  `rate` set('0','1','2','3','4','5') NOT NULL default '0',
  `state` set('0','1') NOT NULL default '0',
  `counter` int(11) NOT NULL default '0',
  `release` tinytext NOT NULL,
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `arto_license`
-- 

CREATE TABLE `arto_license` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(200) NOT NULL default '',
  `link` varchar(255) NOT NULL default '',
  `description` varchar(255) NOT NULL default '',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `arto_types`
-- 

CREATE TABLE `arto_types` (
  `id` int(11) NOT NULL auto_increment,
  `type` varchar(200) NOT NULL default '',
  `parent_id` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `arto_users`
-- 

CREATE TABLE `arto_users` (
  `id` int(11) NOT NULL auto_increment,
  `uname` varchar(30) NOT NULL default '',
  `password` varchar(30) NOT NULL default '',
  `name` varchar(120) NOT NULL default '',
  `email` varchar(200) NOT NULL default '',
  `web` varchar(200) default NULL,
  `state` set('0','1','2','3') NOT NULL default '',
  `typo` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

INSERT INTO `arto_types` VALUES (1, 'Duvar Kağıdı', 0);
INSERT INTO `arto_types` VALUES (2, 'Temalar', 0);
INSERT INTO `arto_types` VALUES (3, 'Müzikler', 0);
INSERT INTO `arto_types` VALUES (4, 'Pardus', 1);
INSERT INTO `arto_types` VALUES (5, 'KDE', 1);
INSERT INTO `arto_types` VALUES (6, 'KDE', 2);
INSERT INTO `arto_types` VALUES (7, 'amaroK', 2);
INSERT INTO `arto_types` VALUES (8, 'Kopete', 2);
INSERT INTO `arto_types` VALUES (9, 'Ekran Görüntüleri', 1);
INSERT INTO `arto_types` VALUES (10, 'Sistem', 3);
INSERT INTO `arto_types` VALUES (11, 'Pardus', 3);

INSERT INTO `arto_users` VALUES (1, 'pardusman', 'ffd03373047a3390328e3d63520f9db6', 'PardusMan', 'arto@uludag.org.tr', 'http://sanat.uludag.org.tr', '0', '0');

INSERT INTO `arto_license` VALUES (1, 'CC Attribution-ShareAlike', 'http://creativecommons.org/licenses/by-sa/2.0/', 'Share Alike. If you alter, transform, or build upon this work, you may distribute the resulting work only under a license identical to this one.');
INSERT INTO `arto_license` VALUES (2, 'GNU General Public License', 'http://creativecommons.org/licenses/GPL/2.0/', 'The GNU General Public License is a Free Software license. Like any Free Software license, it grants to you the four following freedoms:\r\n\r\n   0. The freedom to run the program for any purpose.\r\n   1. The freedom to study how the program works and adapt i');