-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema refrigerator
-- -----------------------------------------------------
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User` (
  `ID` VARCHAR(20) NOT NULL,
  `name` VARCHAR(20) NOT NULL,
  `PSW` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Refri`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Refri` (
  `Refri_ID` VARCHAR(20) NOT NULL,
  `Refri_Cat` VARCHAR(45) NOT NULL,
  `User_ID` VARCHAR(45) NULL,
  PRIMARY KEY (`Refri_ID`),
  INDEX `User_ID_idx` (`User_ID` ASC) VISIBLE,
  CONSTRAINT `User_ID_ref`
    FOREIGN KEY (`User_ID`)
    REFERENCES `mydb`.`User` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`category` (
  `cat_id` VARCHAR(45) NOT NULL,
  `cat_name` VARCHAR(45) NOT NULL,
  `exp_day` DATE NOT NULL,
  PRIMARY KEY (`cat_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`contain`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`contain` (
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
    REFERENCES `mydb`.`Refri` (`Refri_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `cat_id_con`
    FOREIGN KEY (`cat_id`)
    REFERENCES `mydb`.`category` (`cat_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`history` (
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
    REFERENCES `mydb`.`User` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_history_contain1`
    FOREIGN KEY (`contain_Refri_ID` , `contain_food_name` , `contain_input_date` , `contain_exp_date`)
    REFERENCES `mydb`.`contain` (`Refri_ID` , `food_name` , `input_date` , `exp_date`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`notification`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`notification` (
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
    REFERENCES `mydb`.`User` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Refri_ID_note`
    FOREIGN KEY (`Refri_ID`)
    REFERENCES `mydb`.`Refri` (`Refri_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_notification_contain1`
    FOREIGN KEY (`contain_Refri_ID` , `contain_food_name` , `contain_input_date` , `contain_exp_date`)
    REFERENCES `mydb`.`contain` (`Refri_ID` , `food_name` , `input_date` , `exp_date`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
