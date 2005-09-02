-- Server sürümü: 4.1.12
-- Veritabanı: `pardil_py`

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `groups`
-- 

CREATE TABLE groups (
  gid int(10) unsigned NOT NULL auto_increment,
  label varchar(32) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (gid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=6;

-- 
-- Tablo döküm verisi `groups`
-- 

INSERT INTO groups (gid, label) VALUES (1, 'Site Yöneticileri');
INSERT INTO groups (gid, label) VALUES (2, 'Geliştiriciler');
INSERT INTO groups (gid, label) VALUES (3, 'Editörler');
INSERT INTO groups (gid, label) VALUES (4, 'Katkıcılar');
INSERT INTO groups (gid, label) VALUES (5, 'Kullanıcılar');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `proposals`
-- 

CREATE TABLE proposals (
  pid int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  startup datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (pid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2;

-- 
-- Tablo döküm verisi `proposals`
-- 

INSERT INTO proposals (pid, uid, startup) VALUES (1, 1, '0000-00-00 00:00:00');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `proposals_comments`
-- 

CREATE TABLE proposals_comments (
  cid int(10) unsigned NOT NULL auto_increment,
  pid int(10) unsigned NOT NULL default '0',
  uid int(10) unsigned NOT NULL default '0',
  content text collate utf8_turkish_ci NOT NULL,
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (cid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2;

-- 
-- Tablo döküm verisi `proposals_comments`
-- 

INSERT INTO proposals_comments (cid, pid, uid, title, content) VALUES (1, 1, 1, 'İyi, hoş da...', 'İyi, hoş da, kardeşim bir an önce bitirin şu öneri sistemini.');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `proposals_versions`
-- 

CREATE TABLE proposals_versions (
  vid int(10) unsigned NOT NULL auto_increment,
  pid int(10) unsigned NOT NULL default '0',
  version varchar(16) collate utf8_turkish_ci NOT NULL default '0',
  title varchar(100) collate utf8_turkish_ci NOT NULL default '',
  summary text collate utf8_turkish_ci NOT NULL,
  purpose text collate utf8_turkish_ci NOT NULL,
  content text collate utf8_turkish_ci NOT NULL,
  solution text collate utf8_turkish_ci NOT NULL,
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  changelog tinytext collate utf8_turkish_ci NOT NULL,
  PRIMARY KEY  (vid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2 ;

-- 
-- Tablo döküm verisi `proposals_versions`
-- 

INSERT INTO proposals_versions (vid, pid, version, title, content, timeB, changelog) VALUES (1, 1, '1.0.0', 'Pardus İyileştirme Listesi', '...<br/>\r\n...<br/>\r\n...<br/>\r\n...<br/>\r\n...<br/>\r\n...<br/>\r\n...<br/>\r\n...<br/>', '0000-00-00 00:00:00', 'İlk sürüm');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `rel_groups`
-- 

CREATE TABLE rel_groups (
  relid int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  gid int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (relid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=3 ;

-- 
-- Tablo döküm verisi `rel_groups`
-- 

INSERT INTO rel_groups (relid, uid, gid) VALUES (1, 1, 1);
INSERT INTO rel_groups (relid, uid, gid) VALUES (2, 2, 4);

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `rel_maintainers`
-- 

CREATE TABLE rel_maintainers (
  relid int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  pid int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (relid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=1 ;

-- 
-- Tablo döküm verisi `rel_maintainers`
-- 


-- --------------------------------------------------------

-- 
-- Tablo yapısı : `rel_rights`
-- 

CREATE TABLE rel_rights (
  relid int(10) unsigned NOT NULL auto_increment,
  rid int(10) unsigned NOT NULL default '0',
  gid int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (relid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=3 ;

-- 
-- Tablo döküm verisi `rel_rights`
-- 

INSERT INTO rel_rights (relid, rid, gid) VALUES (1, 1, 1);
INSERT INTO rel_rights (relid, rid, gid) VALUES (2, 2, 4);

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `rights`
-- 

CREATE TABLE rights (
  rid int(10) unsigned NOT NULL auto_increment,
  category varchar(32) collate utf8_turkish_ci NOT NULL default '',
  keyword varchar(32) collate utf8_turkish_ci NOT NULL default '',
  label varchar(100) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (rid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=5 ;

-- 
-- Tablo döküm verisi `rights`
-- 

INSERT INTO rights (rid, category, keyword, label) VALUES (1, 'Yönetim', 'administrate', 'Yönetici sayfasına erişebilir.');
INSERT INTO rights (rid, category, keyword, label) VALUES (2, 'Öneriler', 'proposals_add', 'Öneri ekleyebilir.');
INSERT INTO rights (rid, category, keyword, label) VALUES (3, 'Öneriler', 'proposals_comment', 'Önerilere yorum ekleyebilir.');
INSERT INTO rights (rid, category, keyword, label) VALUES (4, 'Öneriler', 'proposals_vote', 'Önerilere oy verebilir.');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `sessions`
-- 

CREATE TABLE sessions (
  sid varchar(32) collate utf8_turkish_ci NOT NULL default '',
  uid int(10) unsigned NOT NULL default '0',
  timeB int(15) NOT NULL default '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- 
-- Tablo döküm verisi `sessions`
-- 

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `users`
-- 

CREATE TABLE users (
  uid int(10) unsigned NOT NULL auto_increment,
  username varchar(32) collate utf8_turkish_ci NOT NULL default '',
  `password` varchar(32) collate utf8_turkish_ci NOT NULL default '',
  email varchar(64) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (uid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci PACK_KEYS=0 AUTO_INCREMENT=3 ;

-- 
-- Tablo döküm verisi `users`
-- 

INSERT INTO users (uid, username, password, email) VALUES (1, 'pardil', 'b7b5d272b4f7fb67bd323c3b2f86bcb2', 'pardil@uludag.org.tr');
INSERT INTO users (uid, username, password, email) VALUES (2, 'test', '0ed2aa90d35d6ef925c40d26b90ad970', 'test@test.test');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `proposals_pending`
-- 

CREATE TABLE `proposals_pending` (
  `tpid` int(10) unsigned NOT NULL auto_increment,
  `uid` int(10) unsigned NOT NULL default '0',
  `title` varchar(100) collate utf8_turkish_ci NOT NULL default '',
  `summary` text collate utf8_turkish_ci NOT NULL,
  `purpose` text collate utf8_turkish_ci NOT NULL,
  `content` text collate utf8_turkish_ci NOT NULL,
  `solution` text collate utf8_turkish_ci NOT NULL,
  `timeB` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`tpid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : `users_pending`
-- 

CREATE TABLE `users_pending` (
  `pid` int(10) unsigned NOT NULL auto_increment,
  `username` varchar(32) collate utf8_turkish_ci NOT NULL default '',
  `password` varchar(32) collate utf8_turkish_ci NOT NULL default '',
  `email` varchar(64) collate utf8_turkish_ci NOT NULL default '',
  `code` varchar(32) collate utf8_turkish_ci NOT NULL default '',
  `timeB` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`pid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
        

CREATE TABLE users_passcodes (
  id int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  code varchar(32) collate utf8_turkish_ci NOT NULL default '',
  timeB int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
