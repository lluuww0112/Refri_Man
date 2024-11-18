SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- 스키마 선택
drop database if exists Refri;
create database if not exists Refri;
USE `refri`;

-- 테이블 생성 구문
CREATE TABLE IF NOT EXISTS `refri`.`User` (
  `ID` VARCHAR(20) NOT NULL,
  `name` VARCHAR(20) NOT NULL,
  `PSW` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `refri`.`Refri` (
  `Refri_ID` VARCHAR(20) NOT NULL,
  `Refri_Cat` VARCHAR(45) NOT NULL,
  `User_ID` VARCHAR(45) NULL,
  PRIMARY KEY (`Refri_ID`),
  INDEX `User_ID_idx` (`User_ID` ASC) VISIBLE,
  CONSTRAINT `User_ID_ref`
    FOREIGN KEY (`User_ID`)
    REFERENCES `refri`.`User` (`ID`)
    ON DELETE cascade
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `refri`.`category` (
  `cat_id` VARCHAR(45) NOT NULL,
  `cat_name` VARCHAR(45) NOT NULL,
  `exp_day` INT NULL,
  PRIMARY KEY (`cat_id`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `refri`.`contain` (
  `Refri_ID` VARCHAR(20) NOT NULL,
  `food_name` VARCHAR(45) NOT NULL,
  `input_date` DATE NOT NULL,
  `exp_date` DATE NOT NULL,
  `cat_id` VARCHAR(45) NOT NULL,
  `count` INT NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Refri_ID`, `food_name`, `input_date`, `exp_date`),
  INDEX `cat_id_idx` (`cat_id` ASC) VISIBLE,
  CONSTRAINT `Refri_ID_con`
    FOREIGN KEY (`Refri_ID`)
    REFERENCES `refri`.`Refri` (`Refri_ID`)
    ON DELETE cascade
    ON UPDATE NO ACTION,
  CONSTRAINT `cat_id_con`
    FOREIGN KEY (`cat_id`)
    REFERENCES `refri`.`category` (`cat_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `refri`.`history` (
  `User_ID` VARCHAR(20) NOT NULL,
  `food_name` VARCHAR(45) NOT NULL,
  `input_date` DATE NOT NULL,
  `exp_date` DATE NOT NULL,
  `Refri_ID` VARCHAR(20) NOT NULL,
  `contain_Refri_ID` VARCHAR(20) NOT NULL,
  `contain_food_name` VARCHAR(45) NOT NULL,
  `contain_input_date` DATE NOT NULL,
  `contain_exp_date` DATE NOT NULL,
  INDEX `User_ID_idx` (`User_ID` ASC) VISIBLE,
  PRIMARY KEY (`contain_Refri_ID`, `contain_food_name`, `contain_input_date`, `contain_exp_date`),
  CONSTRAINT `User_ID_history`
    FOREIGN KEY (`User_ID`)
    REFERENCES `refri`.`User` (`ID`)
    ON DELETE cascade
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_history_contain1`
    FOREIGN KEY (`contain_Refri_ID` , `contain_food_name` , `contain_input_date` , `contain_exp_date`)
    REFERENCES `refri`.`contain` (`Refri_ID` , `food_name` , `input_date` , `exp_date`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `refri`.`notification` (
  `User_id` VARCHAR(20) NOT NULL,
  `Refri_ID` VARCHAR(20) NOT NULL,
  `contain_Refri_ID` VARCHAR(20) NOT NULL,
  `contain_food_name` VARCHAR(45) NOT NULL,
  `contain_input_date` DATE NOT NULL,
  `contain_exp_date` DATE NOT NULL,
  INDEX `User_ID_idx` (`User_id` ASC) VISIBLE,
  INDEX `Refri_ID_idx` (`Refri_ID` ASC) VISIBLE,
  PRIMARY KEY (`contain_Refri_ID`, `contain_food_name`, `contain_input_date`, `contain_exp_date`),
  CONSTRAINT `User_ID_note`
    FOREIGN KEY (`User_id`)
    REFERENCES `refri`.`User` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Refri_ID_note`
    FOREIGN KEY (`Refri_ID`)
    REFERENCES `refri`.`Refri` (`Refri_ID`)
    ON DELETE cascade
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_notification_contain1`
    FOREIGN KEY (`contain_Refri_ID` , `contain_food_name` , `contain_input_date` , `contain_exp_date`)
    REFERENCES `refri`.`contain` (`Refri_ID` , `food_name` , `input_date` , `exp_date`)
    ON DELETE cascade
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
