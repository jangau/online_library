CREATE TABLE `library_donate` (
	`id_donate` INT(11) NOT NULL AUTO_INCREMENT,
	`title` VARCHAR(100) NOT NULL DEFAULT '0',
	`author` VARCHAR(100) NOT NULL DEFAULT '0',
	`genre` VARCHAR(100) NOT NULL DEFAULT '0',
	`ISBN` VARCHAR(13) NOT NULL DEFAULT '0',
	`user_id` INT(11) NOT NULL DEFAULT '0',
	PRIMARY KEY (`id_donate`),
	INDEX `FK_library_donate_auth_user` (`user_id`),
	CONSTRAINT `FK_library_donate_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
);