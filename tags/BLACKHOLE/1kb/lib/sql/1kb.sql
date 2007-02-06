-- 
-- Tablo yapısı : `1kbComments`
-- 

CREATE TABLE `1kbComments` (
  `ID` int(10) unsigned NOT NULL auto_increment,
  `UID` int(11) NOT NULL default '0',
  `DataID` int(11) NOT NULL default '0',
  `Comment` tinytext NOT NULL,
  `Date` varchar(12) NOT NULL default '',
  `State` set('0','1') NOT NULL default '0',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `1kbData`
-- 

CREATE TABLE `1kbData` (
  `ID` int(10) unsigned NOT NULL auto_increment,
  `UID` int(11) NOT NULL default '0',
  `Question` varchar(250) NOT NULL default '',
  `RelatedQuestion` int(11) NOT NULL default '0',
  `Answer` text NOT NULL,
  `RelatedAnswer` int(11) NOT NULL default '0',
  `Date` varchar(12) NOT NULL default '',
  `State` set('0','1') NOT NULL default '0',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
