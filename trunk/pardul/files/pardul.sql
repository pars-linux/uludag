-- phpMyAdmin SQL Dump
-- version 2.6.1-pl3
-- http://www.phpmyadmin.net
-- 
-- Host: localhost
-- Generation Time: Mar 20, 2005 at 10:49 PM
-- Server version: 4.0.22
-- PHP Version: 4.3.9
-- 
-- Database: `pardul`
-- 

-- --------------------------------------------------------

-- 
-- Table structure for table `brand`
-- 

DROP TABLE IF EXISTS `brand`;
CREATE TABLE `brand` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(32) NOT NULL default '',
  PRIMARY KEY  (`id`),
  KEY `name` (`name`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Table structure for table `comment`
-- 

DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL auto_increment,
  `mpvs_id` int(11) NOT NULL default '0',
  `comment` text NOT NULL,
  `emailaddr` varchar(64) NOT NULL default '',
  `rname` varchar(64) NOT NULL default '',
  `entry_date` date NOT NULL default '0000-00-00',
  PRIMARY KEY  (`id`),
  KEY `model_id` (`mpvs_id`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Table structure for table `function`
-- 

DROP TABLE IF EXISTS `function`;
CREATE TABLE `function` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(16) NOT NULL default '',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Table structure for table `group`
-- 

DROP TABLE IF EXISTS `group`;
CREATE TABLE `group` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(32) NOT NULL default '',
  `managed_by` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `name` (`name`),
  KEY `managed_by` (`managed_by`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Table structure for table `group_brand`
-- 

DROP TABLE IF EXISTS `group_brand`;
CREATE TABLE `group_brand` (
  `id` int(11) NOT NULL auto_increment,
  `group_id` int(11) NOT NULL default '0',
  `brand_id` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `group_id` (`group_id`),
  KEY `brand_id` (`brand_id`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Table structure for table `model`
-- 

DROP TABLE IF EXISTS `model`;
CREATE TABLE `model` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(32) NOT NULL default '',
  `groupbrand_id` int(11) NOT NULL default '0',
  `status` enum('ACTIVE','PASSIVE') NOT NULL default 'ACTIVE',
  PRIMARY KEY  (`id`),
  KEY `name` (`name`),
  KEY `groupbrand_id` (`groupbrand_id`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Table structure for table `model_pv_status`
-- 

DROP TABLE IF EXISTS `model_pv_status`;
CREATE TABLE `model_pv_status` (
  `id` int(11) NOT NULL auto_increment,
  `model_id` int(11) NOT NULL default '0',
  `pv_id` int(11) NOT NULL default '0',
  `status_id` int(11) NOT NULL default '0',
  `status_text` text NOT NULL,
  `entry_date` date NOT NULL default '0000-00-00',
  `status` enum('ACTIVE','PASSIVE') NOT NULL default 'ACTIVE',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Table structure for table `pardus_version`
-- 

DROP TABLE IF EXISTS `pardus_version`;
CREATE TABLE `pardus_version` (
  `id` int(11) NOT NULL auto_increment,
  `pv_text` varchar(32) NOT NULL default '',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Table structure for table `role`
-- 

DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL auto_increment,
  `rolename` varchar(32) NOT NULL default '',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `rolename` (`rolename`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Table structure for table `role_function`
-- 

DROP TABLE IF EXISTS `role_function`;
CREATE TABLE `role_function` (
  `id` int(11) NOT NULL auto_increment,
  `role_id` int(11) NOT NULL default '0',
  `function_id` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Table structure for table `status`
-- 

DROP TABLE IF EXISTS `status`;
CREATE TABLE `status` (
  `id` int(11) NOT NULL auto_increment,
  `status_name` varchar(16) NOT NULL default '',
  `description` text NOT NULL,
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Table structure for table `user`
-- 

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(32) NOT NULL default '',
  `password` varchar(64) NOT NULL default '',
  `rname` varchar(32) NOT NULL default '',
  `emailaddr` varchar(128) NOT NULL default '',
  `role_id` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;
