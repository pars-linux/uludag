DROP TABLE IF EXISTS `components`;
CREATE TABLE `components` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(128) NOT NULL,
  `packager` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `components_descriptions`;
CREATE TABLE `components_descriptions` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `component` int(10) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `components_localnames`;
CREATE TABLE `components_localnames` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `component` int(10) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `localname` varchar(128) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `components_summaries`;
CREATE TABLE `components_summaries` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `component` int(10) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `summary` text NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `history`;
CREATE TABLE `history` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `release` int(10) unsigned NOT NULL,
  `version` varchar(32) NOT NULL,
  `modifydate` date NOT NULL,
  `packager` int(10) unsigned NOT NULL,
  `comment` text NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `licenses`;
CREATE TABLE `licenses` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `packagers`;
CREATE TABLE `packagers` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(128) NOT NULL,
  `email` varchar(128) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `packages`;
CREATE TABLE `packages` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `packages_deps`;
CREATE TABLE `packages_deps` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `package` int(10) unsigned NOT NULL,
  `dep` varchar(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `patches`;
CREATE TABLE `patches` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `file` varchar(128) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `sources`;
CREATE TABLE `sources` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(32) NOT NULL,
  `homepage` varchar(256) NOT NULL,
  `packager` int(10) unsigned NOT NULL,
  `is_a` int(10) unsigned NOT NULL,
  `icon` varchar(32) NOT NULL,
  `archive_sum` varchar(40) NOT NULL,
  `archive_url` varchar(256) NOT NULL,
  `release` int(10) unsigned NOT NULL default '1',
  `version` varchar(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `sources_components`;
CREATE TABLE `sources_components` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `component` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `sources_deps`;
CREATE TABLE `sources_deps` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `dep` varchar(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `sources_descriptions`;
CREATE TABLE `sources_descriptions` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `sources_licenses`;
CREATE TABLE `sources_licenses` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `license` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `sources_patches`;
CREATE TABLE `sources_patches` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `patch` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `sources_summaries`;
CREATE TABLE `sources_summaries` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `summary` text NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_components`;
CREATE TABLE `tmp_components` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(128) NOT NULL,
  `packager` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_components_descriptions`;
CREATE TABLE `tmp_components_descriptions` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `component` int(10) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_components_localnames`;
CREATE TABLE `tmp_components_localnames` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `component` int(10) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `localname` varchar(128) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_components_summaries`;
CREATE TABLE `tmp_components_summaries` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `component` int(10) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `summary` text NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_history`;
CREATE TABLE `tmp_history` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `release` int(10) unsigned NOT NULL,
  `version` varchar(32) NOT NULL,
  `modifydate` date NOT NULL,
  `packager` int(10) unsigned NOT NULL,
  `comment` text NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_licenses`;
CREATE TABLE `tmp_licenses` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_packagers`;
CREATE TABLE `tmp_packagers` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(128) NOT NULL,
  `email` varchar(128) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_packages`;
CREATE TABLE `tmp_packages` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_packages_deps`;
CREATE TABLE `tmp_packages_deps` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `package` int(10) unsigned NOT NULL,
  `dep` varchar(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_patches`;
CREATE TABLE `tmp_patches` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `file` varchar(128) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_sources`;
CREATE TABLE `tmp_sources` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(32) NOT NULL,
  `homepage` varchar(256) NOT NULL,
  `packager` int(10) unsigned NOT NULL,
  `is_a` int(10) unsigned NOT NULL,
  `icon` varchar(32) NOT NULL,
  `archive_sum` varchar(40) NOT NULL,
  `archive_url` varchar(256) NOT NULL,
  `release` int(10) unsigned NOT NULL default '1',
  `version` varchar(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_sources_components`;
CREATE TABLE `tmp_sources_components` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `component` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_sources_deps`;
CREATE TABLE `tmp_sources_deps` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `dep` varchar(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_sources_descriptions`;
CREATE TABLE `tmp_sources_descriptions` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_sources_licenses`;
CREATE TABLE `tmp_sources_licenses` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `license` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_sources_patches`;
CREATE TABLE `tmp_sources_patches` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `patch` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_sources_summaries`;
CREATE TABLE `tmp_sources_summaries` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `source` int(10) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `summary` text NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tmp_types`;
CREATE TABLE `tmp_types` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `types`;
CREATE TABLE `types` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
