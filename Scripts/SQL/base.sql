----------------------------------------------------------------------------------------------------------------
-- Création de la base de données ------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS `data_for_figure`;
USE `data_for_figure`;

----------------------------------------------------------------------------------------------------------------
-- Re-création de la table -------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `filtred_data`;

CREATE TABLE IF NOT EXISTS `filtred_data` (
    `country_id` SMALLINT(5) PRIMARY KEY AUTO_INCREMENT,
    `country_name` VARCHAR(100) NOT NULL,
    `regional_indicator` VARCHAR(100) NOT NULL,
    `ladder_score` FLOAT NOT NULL,
    `standard_error_of_ladder_score` FLOAT NOT NULL,
    `upperwhisker` FLOAT NOT NULL,
    `lowerwhisker` FLOAT NOT NULL,
    `logged_gdp_per_capita` FLOAT NOT NULL,
    `social_support` FLOAT NOT NULL,
    `healthy_life_expectancy` FLOAT NOT NULL,
    `freedom_to_make_life_choices` FLOAT NOT NULL,
    `generosity` FLOAT NOT NULL,
    `perceptions_of_corruption` FLOAT NOT NULL,
    `ladder_score_in_dystopia` FLOAT NOT NULL,
    `explained_by_log_gdp_per_capita` FLOAT NOT NULL,
    `explained_by_social_support` FLOAT NOT NULL,
    `explained_by_healthy_life_expectancy` FLOAT NOT NULL,
    `explained_by_freedom_to_make_life_choices` FLOAT NOT NULL,
    `explained_by_generosity` FLOAT NOT NULL, 
    `explained_by_perceptions_of_corruption` FLOAT NOT NULL,
    `dystopia_plus_residual` FLOAT NOT NULL
)
ENGINE = InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

----------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------