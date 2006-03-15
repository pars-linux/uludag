-- 
-- Veritabanı: `pardul`
-- 

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulActionCompatibility`
-- 

CREATE TABLE `pardulActionCompatibility` (
  `ID` int(11) NOT NULL auto_increment,
  `DistID` int(11) NOT NULL default '0',
  `PlatformID` int(11) NOT NULL default '0',
  `HWID` bigint(20) NOT NULL default '0',
  `HWState` set('F','S','N') NOT NULL default '',
  `ToDoToWork` text,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulCategories`
-- 

CREATE TABLE `pardulCategories` (
  `ID` int(11) NOT NULL auto_increment,
  `CategoryName` varchar(32) NOT NULL default '',
  `ParentID` int(11) NOT NULL default '0',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulDistribution`
-- 

CREATE TABLE `pardulDistribution` (
  `ID` int(11) NOT NULL auto_increment,
  `DistVersion` varchar(32) NOT NULL default '',
  `DistName` varchar(32) NOT NULL default 'Pardus',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulHardwares`
-- 

CREATE TABLE `pardulHardwares` (
  `ID` bigint(20) NOT NULL auto_increment,
  `HWProductName` varchar(250) NOT NULL default '',
  `HWVendorID` bigint(20) NOT NULL default '0',
  `HWDeviceID` varchar(24) NOT NULL default '',
  `HWBusType` varchar(24) NOT NULL default '',
  `HWCategoryID` int(11) NOT NULL default '0',
  `HWAddDate` varchar(12) NOT NULL default '',
  `HWUpdateDate` varchar(12) NOT NULL default '',
  `Status` set('1','0') NOT NULL default '0',
  `UserID` int(11) NOT NULL default '0',
  `SuperUserID` int(11) NOT NULL default '0',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulPlatform`
-- 

CREATE TABLE `pardulPlatform` (
  `ID` int(11) NOT NULL auto_increment,
  `Platform` varchar(32) NOT NULL default '',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulUsers`
-- 

CREATE TABLE `pardulUsers` (
  `ID` int(11) NOT NULL auto_increment,
  `UserName` varchar(32) NOT NULL default '',
  `UserPass` varchar(32) NOT NULL default '',
  `UserRealName` varchar(32) NOT NULL default '',
  `UserEmail` varchar(72) NOT NULL default '',
  `UserWeb` varchar(72) NOT NULL default '',
  `UserState` set('G','SA','A') NOT NULL default 'G',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulVendors`
-- 

CREATE TABLE `pardulVendors` (
  `id` int(11) NOT NULL auto_increment,
  `VendorName` varchar(200) NOT NULL default '',
  `VendorURL` varchar(200) NOT NULL default '---',
  `VendorID` varchar(24) NOT NULL default '---',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulComments`
-- 

CREATE TABLE `pardulComments` (
  `ID` bigint(20) NOT NULL auto_increment,
  `HWID` bigint(20) NOT NULL default '0',
  `UID` int(11) NOT NULL default '0',
  `Comment` text NOT NULL,
  `AddDate` varchar(12) NOT NULL default '',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
