CREATE TABLE `tb_short_link` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `short_key` varchar(30) NOT NULL,
  `source_url` varchar(300) NOT NULL,
  `created_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `short_key` (`short_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

