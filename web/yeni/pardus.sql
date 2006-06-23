-- phpMyAdmin SQL Dump
-- version 2.8.1
-- http://www.phpmyadmin.net
--
-- Sunucu: localhost
-- Çıktı Tarihi: Haziran 23, 2006 at 03:02 PM
-- Server sürümü: 4.1.19
-- PHP Sürümü: 5.1.4
--
-- Veritabanı: `Pardus`
--

-- --------------------------------------------------------

--
-- Tablo yapısı : `Logs`
--

CREATE TABLE `Logs` (
  `Id` bigint(20) NOT NULL auto_increment,
  `Date` varchar(6) NOT NULL default '',
  `IP` varchar(16) NOT NULL default '',
  `Str` varchar(250) NOT NULL default '',
  `Node` varchar(250) NOT NULL default '',
  PRIMARY KEY  (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tablo yapısı : `News`
--

CREATE TABLE `News` (
  `ID` int(11) NOT NULL auto_increment,
  `Lang` set('TR','EN') NOT NULL default 'TR',
  `Title` varchar(250) NOT NULL default '',
  `Date` varchar(5) NOT NULL default '',
  `Content` text NOT NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- Tablo yapısı : `Pages`
--

CREATE TABLE `Pages` (
  `ID` int(11) NOT NULL auto_increment,
  `Lang` set('TR','EN') NOT NULL default 'TR',
  `Parent` set('B','K','G','R') NOT NULL default '',
  `Type` set('D','P') NOT NULL default '',
  `Title` varchar(250) NOT NULL default '',
  `Content` text NOT NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
