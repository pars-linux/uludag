CREATE TABLE `users` (
  `uid` int(10) unsigned NOT NULL auto_increment,
  `username` varchar(32) collate utf8_turkish_ci NOT NULL default '',
  `password` varchar(32) collate utf8_turkish_ci NOT NULL default '',
  `email` varchar(64) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci PACK_KEYS=0 AUTO_INCREMENT=1;

CREATE TABLE groups (
  gid int(10) unsigned NOT NULL auto_increment,
  name varchar(16) collate utf8_turkish_ci NOT NULL default '',
  label varchar(32) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (gid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=3 ;

INSERT INTO groups (gid, name, label) VALUES (1, 'developer', 'Geliştirici');
INSERT INTO groups (gid, name, label) VALUES (2, 'contributor', 'Katkıcı');
