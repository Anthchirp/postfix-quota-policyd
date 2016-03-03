/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE IF NOT EXISTS `pypolicyd` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `pypolicyd`;

CREATE TABLE IF NOT EXISTS `auth` (
  `username` varchar(50) NOT NULL,
  `password` varchar(250) NOT NULL,
  `source` varchar(20) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40000 ALTER TABLE `auth` DISABLE KEYS */;
REPLACE INTO `auth` (`username`, `password`, `source`) VALUES
	('pytest_dummy_user_1', '$1$somepass', 'pytest'),
	('pytest_dummy_user_2', '$1$somepass', 'pytest');
/*!40000 ALTER TABLE `auth` ENABLE KEYS */;

CREATE TABLE IF NOT EXISTS `smtplogin` (
  `username` varchar(50) NOT NULL,
  `source` varchar(20) NOT NULL,
  `locked` enum('Y','N') NOT NULL DEFAULT 'N',
  `password` varchar(250) NOT NULL,
  `authcount` int(10) unsigned NOT NULL DEFAULT '0',
  `limit` int(10) unsigned NOT NULL DEFAULT '100',
  `dynlimit` int(10) unsigned NOT NULL DEFAULT '100',
  `lastseen` datetime DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

/*!40000 ALTER TABLE `smtplogin` DISABLE KEYS */;
REPLACE INTO `smtplogin` (`username`, `source`, `locked`, `password`, `authcount`, `limit`, `dynlimit`, `lastseen`) VALUES
	('pytest_dummy_user_1', 'pytest', 'N', '$1$differentpass', 0, 3, 3, '2016-03-02 21:34:08');
DELETE FROM `smtplogin` WHERE `username` = 'pytest_dummy_user_2' AND `source`= 'pytest';
/*!40000 ALTER TABLE `smtplogin` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
