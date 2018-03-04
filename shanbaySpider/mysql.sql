CREATE TABLE IF NOT EXISTS `daily_translation`(
   `daily_translation_id` INT UNSIGNED AUTO_INCREMENT,
   `daily_translation_title` VARCHAR(100) NOT NULL,
   `daily_translation_author` VARCHAR(40) NOT NULL,
   `daily_translation_date` DATE,
   PRIMARY KEY ( `daily_translation_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;