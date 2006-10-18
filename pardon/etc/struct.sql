-- 
-- Tablo yapısı : `pardulActionCompatibility`
-- 

CREATE TABLE IF NOT EXISTS `pardulActionCompatibility` (
  `ID` int(11) NOT NULL auto_increment,
  `DistID` int(11) NOT NULL default '0',
  `PlatformID` int(11) NOT NULL default '0',
  `HWID` bigint(20) NOT NULL default '0',
  `HWState` set('F','S','N','X') NOT NULL default '',
  PRIMARY KEY  (`ID`)
) TYPE=MyISAM AUTO_INCREMENT=255 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulBusTypes`
-- 

CREATE TABLE IF NOT EXISTS `pardulBusTypes` (
  `Type` varchar(30) NOT NULL default '',
  PRIMARY KEY  (`Type`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulCategories`
-- 

CREATE TABLE IF NOT EXISTS `pardulCategories` (
  `ID` int(11) NOT NULL auto_increment,
  `CategoryName` varchar(32) NOT NULL default '',
  `ParentID` int(11) NOT NULL default '0',
  PRIMARY KEY  (`ID`)
) TYPE=MyISAM AUTO_INCREMENT=33 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulComments`
-- 

CREATE TABLE IF NOT EXISTS `pardulComments` (
  `ID` bigint(20) NOT NULL auto_increment,
  `HWID` bigint(20) NOT NULL default '0',
  `UID` int(11) NOT NULL default '0',
  `Comment` text NOT NULL,
  `AddDate` varchar(12) NOT NULL default '',
  PRIMARY KEY  (`ID`)
) TYPE=MyISAM AUTO_INCREMENT=6 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulDistribution`
-- 

CREATE TABLE IF NOT EXISTS `pardulDistribution` (
  `ID` int(11) NOT NULL auto_increment,
  `DistVersion` varchar(32) NOT NULL default '',
  `DistName` varchar(32) NOT NULL default 'Pardus',
  PRIMARY KEY  (`ID`)
) TYPE=MyISAM AUTO_INCREMENT=9 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulHardwares`
-- 

CREATE TABLE IF NOT EXISTS `pardulHardwares` (
  `ID` bigint(20) NOT NULL auto_increment,
  `HWProductName` varchar(250) NOT NULL default '',
  `HWVendor` varchar(20) NOT NULL default '',
  `HWDeviceID` varchar(24) NOT NULL default '',
  `HWBusType` varchar(24) NOT NULL default '',
  `HWCategoryID` int(11) NOT NULL default '0',
  `HWAddDate` varchar(12) NOT NULL default '',
  `HWUpdateDate` varchar(12) NOT NULL default '',
  `Status` set('1','0') NOT NULL default '0',
  `UserID` int(11) NOT NULL default '0',
  `SuperUserID` int(11) NOT NULL default '0',
  `ToDo` text NOT NULL,
  PRIMARY KEY  (`ID`)
) TYPE=MyISAM AUTO_INCREMENT=93 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulPlatform`
-- 

CREATE TABLE IF NOT EXISTS `pardulPlatform` (
  `ID` int(11) NOT NULL auto_increment,
  `Platform` varchar(32) NOT NULL default '',
  PRIMARY KEY  (`ID`)
) TYPE=MyISAM AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulUsers`
-- 

CREATE TABLE IF NOT EXISTS `pardulUsers` (
  `ID` int(11) NOT NULL auto_increment,
  `UserName` varchar(32) NOT NULL default '',
  `UserPass` varchar(32) NOT NULL default '',
  `UserRealName` varchar(32) NOT NULL default '',
  `UserEmail` varchar(72) NOT NULL default '',
  `UserWeb` varchar(72) NOT NULL default '',
  `UserState` set('G','SA','A','N') NOT NULL default 'N',
  PRIMARY KEY  (`ID`)
) TYPE=MyISAM AUTO_INCREMENT=51 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `pardulVendors`
-- 

CREATE TABLE IF NOT EXISTS `pardulVendors` (
  `VendorName` varchar(25) NOT NULL default '',
  PRIMARY KEY  (`VendorName`)
) TYPE=MyISAM;

