CREATE TABLE `feedback` (
  `no` int(10) unsigned NOT NULL auto_increment,
  `ip` varchar(15) default NULL,
  `submitdate` datetime default NULL,
  `exp` enum('new_user','home_office_user','experienced_user','experienced_admin') default NULL,
  `purpose` set('daily_use','hobby','internet_access','business_use','entertaintment','education') default NULL,
  `use_where` set('home','office','school') default NULL,
  `question` enum('satisfying','good_but','insufficient') default NULL,
  `opinion` text,
  `email` varchar(60) default '',
  `email_announce` char(1) default 'F',
  `hardware` text,
  PRIMARY KEY  (`no`)
) TYPE=MyISAM AUTO_INCREMENT=1;
