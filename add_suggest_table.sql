CREATE TABLE `library_suggest` (
	`id_suggestion` INT(11) NOT NULL AUTO_INCREMENT,
	`title` VARCHAR(100) NOT NULL,
	`author` VARCHAR(100) NOT NULL,
	`user_id` INT(11) NOT NULL,
	PRIMARY KEY (`id_suggestion`),
	INDEX `FK__auth_user` (`user_id`),
	CONSTRAINT `FK__auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
)