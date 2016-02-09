CREATE DATABASE `sXXXXX__tif`;

DROP TABLE IF EXISTS `cache`;
CREATE TABLE `cache` (
  `cache_id` INT(10) UNSIGNED NOT NULL,
  `cache_views` INT UNSIGNED NOT NULL,
  `cache_time` TIMESTAMP NOT NULL,
  PRIMARY KEY (`cache_id`)
) ENGINE=InnoDB;
