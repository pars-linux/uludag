CREATE TABLE `feedback` (
  `no` int(10) unsigned NOT NULL auto_increment,
  `ip` varchar(15) default NULL,
  `submitdate` datetime default NULL,
  `experience` enum('new_user','home_office_user','experienced_user','experienced_admin') default NULL,
  `purpose` set('daily_use','hobby','internet_access','business_use','entertaintment','education') default NULL,
  `use_where` set('home','office','school') default NULL,
  `question` enum('satisfying','good_but','insufficient') default NULL,
  `opinion` text,
  `email` varchar(60) default NULL,
  `email_announce` char(1) default 'F',
  PRIMARY KEY  (`no`)
) TYPE=MyISAM;


CREATE TABLE `hardware` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `feedback` int(10) unsigned NOT NULL default '0',
  `memtotal` int(10) unsigned NOT NULL default '0',
  `swaptotal` int(10) unsigned NOT NULL default '0',
  `cpu_model` varchar(64) NOT NULL default '',
  `cpu_speed` float NOT NULL default '0',
  `kernel` varchar(64) NOT NULL default '',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;
