-- phpMyAdmin SQL Dump
-- version 2.6.1-pl3
-- http://www.phpmyadmin.net
-- 
-- Host: localhost
-- Generation Time: Apr 28, 2005 at 12:12 AM
-- Server version: 4.0.22
-- PHP Version: 4.3.10
-- 
-- Database: `pardul`
-- 

-- --------------------------------------------------------

-- 
-- Table structure for table `brand`
-- 

CREATE TABLE `brand` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(32) NOT NULL default '',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name_2` (`name`)
) TYPE=MyISAM;

-- 
-- Dumping data for table `brand`
-- 


-- --------------------------------------------------------

-- 
-- Table structure for table `comment`
-- 

CREATE TABLE `comment` (
  `id` int(11) NOT NULL auto_increment,
  `mpvs_id` int(11) NOT NULL default '0',
  `comment` text NOT NULL,
  `emailaddr` varchar(64) NOT NULL default '',
  `rname` varchar(64) NOT NULL default '',
  `entry_date` date NOT NULL default '0000-00-00',
  `status` enum('ACTIVE','PASSIVE') NOT NULL default 'ACTIVE',
  PRIMARY KEY  (`id`),
  KEY `model_id` (`mpvs_id`)
) TYPE=MyISAM;

-- 
-- Dumping data for table `comment`
-- 


-- --------------------------------------------------------

-- 
-- Table structure for table `group`
-- 

CREATE TABLE `group` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(32) NOT NULL default '',
  `managed_by` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name_2` (`name`),
  KEY `name` (`name`),
  KEY `managed_by` (`managed_by`)
) TYPE=MyISAM;

-- 
-- Dumping data for table `group`
-- 


-- --------------------------------------------------------

-- 
-- Table structure for table `group_brand`
-- 

CREATE TABLE `group_brand` (
  `id` int(11) NOT NULL auto_increment,
  `group_id` int(11) NOT NULL default '0',
  `brand_id` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `group_id` (`group_id`),
  KEY `brand_id` (`brand_id`)
) TYPE=MyISAM;

-- 
-- Dumping data for table `group_brand`
-- 


-- --------------------------------------------------------

-- 
-- Table structure for table `model`
-- 

CREATE TABLE `model` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(32) NOT NULL default '',
  `groupbrand_id` int(11) NOT NULL default '0',
  `status` enum('ACTIVE','PASSIVE') NOT NULL default 'ACTIVE',
  PRIMARY KEY  (`id`),
  KEY `name` (`name`),
  KEY `groupbrand_id` (`groupbrand_id`)
) TYPE=MyISAM;

-- 
-- Dumping data for table `model`
-- 


-- --------------------------------------------------------

-- 
-- Table structure for table `model_pv_status`
-- 

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

-- 
-- Dumping data for table `model_pv_status`
-- 


-- --------------------------------------------------------

-- 
-- Table structure for table `pardus_version`
-- 

CREATE TABLE `pardus_version` (
  `id` int(11) NOT NULL auto_increment,
  `pv_text` varchar(32) NOT NULL default '',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

-- 
-- Dumping data for table `pardus_version`
-- 


-- --------------------------------------------------------

-- 
-- Table structure for table `role`
-- 

CREATE TABLE `role` (
  `id` int(11) NOT NULL auto_increment,
  `rolename` varchar(32) NOT NULL default '',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `rolename` (`rolename`)
) TYPE=MyISAM;

-- 
-- Dumping data for table `role`
-- 

INSERT INTO `role` VALUES (1, 'admin');
INSERT INTO `role` VALUES (2, 'sub_admin');

-- --------------------------------------------------------

-- 
-- Table structure for table `status`
-- 

CREATE TABLE `status` (
  `id` int(11) NOT NULL auto_increment,
  `status_name` varchar(16) NOT NULL default '',
  `description` text NOT NULL,
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

-- 
-- Dumping data for table `status`
-- 


-- --------------------------------------------------------

-- 
-- Table structure for table `user`
-- 

CREATE TABLE `user` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(32) NOT NULL default '',
  `password` varchar(64) NOT NULL default '',
  `rname` varchar(32) NOT NULL default '',
  `emailaddr` varchar(128) NOT NULL default '',
  `role_id` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`)
) TYPE=MyISAM;

-- 
-- Dumping data for table `user`
-- 

INSERT INTO `user` VALUES (1, 'pardul', '529bb242552ea639', 'pardul', 'pardul@pardul.pardul', 1);
