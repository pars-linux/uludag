CREATE TABLE `users` (
  `uid` int(10) unsigned NOT NULL auto_increment,
  `username` varchar(32) collate utf8_turkish_ci NOT NULL default '',
  `password` varchar(32) collate utf8_turkish_ci NOT NULL default '',
  `email` varchar(64) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci PACK_KEYS=0 AUTO_INCREMENT=1;
