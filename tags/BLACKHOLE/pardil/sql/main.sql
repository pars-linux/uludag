-- Server sürümü: 4.1.12
-- Veritabanı: pardil_py

-- --------------------------------------------------------

-- 
-- Tablo yapısı : groups
-- 

CREATE TABLE groups (
  gid int(10) unsigned NOT NULL auto_increment,
  label varchar(32) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (gid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=1;

-- 
-- Tablo döküm verisi groups
-- 

INSERT INTO groups (gid, label) VALUES (1, 'Site Yöneticileri');
INSERT INTO groups (gid, label) VALUES (2, 'Kullanıcılar');
INSERT INTO groups (gid, label) VALUES (3, 'Geliştiriciler');
INSERT INTO groups (gid, label) VALUES (4, 'Katkıcılar');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : proposals
-- 

CREATE TABLE proposals (
  pid int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  startup datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (pid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : proposals_comments
-- 

CREATE TABLE proposals_comments (
  cid int(10) unsigned NOT NULL auto_increment,
  pid int(10) unsigned NOT NULL default '0',
  uid int(10) unsigned NOT NULL default '0',
  content text collate utf8_turkish_ci NOT NULL,
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (cid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : proposals_versions
-- 

CREATE TABLE proposals_versions (
  vid int(10) unsigned NOT NULL auto_increment,
  pid int(10) unsigned NOT NULL default '0',
  version varchar(16) collate utf8_turkish_ci NOT NULL default '0',
  title varchar(100) collate utf8_turkish_ci NOT NULL default '',
  summary text collate utf8_turkish_ci NOT NULL,
  purpose text collate utf8_turkish_ci NOT NULL,
  content text collate utf8_turkish_ci NOT NULL,
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  changelog tinytext collate utf8_turkish_ci NOT NULL,
  PRIMARY KEY  (vid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : rel_groups
-- 

CREATE TABLE rel_groups (
  relid int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  gid int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (relid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=1;

-- 
-- Tablo döküm verisi rel_groups
-- 

INSERT INTO rel_groups (relid, uid, gid) VALUES (1, 1, 1);

-- --------------------------------------------------------

-- 
-- Tablo yapısı : rel_maintainers
-- 

CREATE TABLE rel_maintainers (
  relid int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  pid int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (relid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : rel_rights
-- 

CREATE TABLE rel_rights (
  relid int(10) unsigned NOT NULL auto_increment,
  rid int(10) unsigned NOT NULL default '0',
  gid int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (relid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : rights
-- 

CREATE TABLE rights (
  rid int(10) unsigned NOT NULL auto_increment,
  category varchar(32) collate utf8_turkish_ci NOT NULL default '',
  keyword varchar(32) collate utf8_turkish_ci NOT NULL default '',
  label varchar(100) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (rid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=5 ;

-- 
-- Tablo döküm verisi rights
-- 

INSERT INTO rights (rid, category, keyword, label) VALUES (2, 'Bildiriler', 'proposals_add', 'Bildiri ekleyebilir.');
INSERT INTO rights (rid, category, keyword, label) VALUES (3, 'Bildiriler', 'proposals_comment', 'Bildirilere yorum ekleyebilir.');
INSERT INTO rights (rid, category, keyword, label) VALUES (4, 'Bildiriler', 'proposals_vote', 'Bildirilere oy verebilir.');
INSERT INTO rights VALUES (6, 'Bildiriler', 'proposals_publish', 'Gönderdiği öneriler hemen yayınlanır.');
INSERT INTO rights VALUES (7, 'Yönetim', 'administrate_usergroups', 'Kullanıcı gruplarını değiştirebilir.');
INSERT INTO rights VALUES (8, 'Yönetim', 'administrate_userrights', 'Erişim haklarını değiştirebilir.');
INSERT INTO rights VALUES (9, 'Yönetim', 'administrate_maintainers', 'Bildiri sorumlularını değiştirebilir.');
INSERT INTO rights VALUES (10, 'Yönetim', 'administrate_pending', 'Bildiri yayınlayabilir.');
INSERT INTO rights VALUES (11, 'Yönetim', 'administrate_comments', 'Yorumları silebilir.');
INSERT INTO rights VALUES (12, 'Yönetim', 'administrate_groups', 'Sisteme grup ekleyebilir.');
INSERT INTO rights VALUES (13, 'Yönetim', 'administrate_rights', 'Sisteme erişim hakkı ekleyebilir.');
INSERT INTO rights VALUES (14, 'Yönetim', 'administrate_proposals', 'Bildirilere müdahale edebilir.');
-- --------------------------------------------------------

-- 
-- Tablo yapısı : sessions
-- 

CREATE TABLE sessions (
  sid varchar(32) collate utf8_turkish_ci NOT NULL default '',
  uid int(10) unsigned NOT NULL default '0',
  timeB int(10) unsigned NOT NULL default '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : users
-- 

CREATE TABLE users (
  uid int(10) unsigned NOT NULL auto_increment,
  username varchar(32) collate utf8_turkish_ci NOT NULL default '',
  password varchar(32) collate utf8_turkish_ci NOT NULL default '',
  email varchar(64) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (uid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci PACK_KEYS=0 AUTO_INCREMENT=1;

-- 
-- Tablo döküm verisi users
-- 

INSERT INTO users (uid, username, password, email) VALUES (1, 'pardil', 'b7b5d272b4f7fb67bd323c3b2f86bcb2', 'pardil@uludag.org.tr');

-- --------------------------------------------------------

-- 
-- Tablo yapısı : proposals_pending
-- 

CREATE TABLE proposals_pending (
  tpid int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  pid int(10) unsigned NOT NULL default '0',
  title varchar(100) collate utf8_turkish_ci NOT NULL default '',
  summary text collate utf8_turkish_ci NOT NULL,
  purpose text collate utf8_turkish_ci NOT NULL,
  content text collate utf8_turkish_ci NOT NULL,
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (tpid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : users_pending
-- 

CREATE TABLE users_pending (
  pid int(10) unsigned NOT NULL auto_increment,
  username varchar(32) collate utf8_turkish_ci NOT NULL default '',
  password varchar(32) collate utf8_turkish_ci NOT NULL default '',
  email varchar(64) collate utf8_turkish_ci NOT NULL default '',
  code varchar(32) collate utf8_turkish_ci NOT NULL default '',
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (pid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
        

CREATE TABLE users_passcodes (
  id int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  code varchar(32) collate utf8_turkish_ci NOT NULL default '',
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

-- 
-- Tablo yapısı : news
-- 

CREATE TABLE news (
  nid int(10) unsigned NOT NULL auto_increment,
  uid int(10) unsigned NOT NULL default '0',
  title varchar(100) collate utf8_turkish_ci NOT NULL default '',
  content text collate utf8_turkish_ci NOT NULL,
  icon varchar(30) collate utf8_turkish_ci NOT NULL default '',
  timeB datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (nid)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
        
