-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: dep_database
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `luchthaven`
--

DROP TABLE IF EXISTS `luchthaven`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `luchthaven` (
  `luchthaven_id` int unsigned NOT NULL AUTO_INCREMENT,
  `airport_code` varchar(10) NOT NULL,
  `naam` varchar(60) NOT NULL,
  PRIMARY KEY (`luchthaven_id`),
  UNIQUE KEY `luchthaven_id_UNIQUE` (`luchthaven_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `luchthaven`
--

LOCK TABLES `luchthaven` WRITE;
/*!40000 ALTER TABLE `luchthaven` DISABLE KEYS */;
INSERT INTO `luchthaven` VALUES (3,'AMS','Amsterdam'),(4,'LHR','Londen Heathrow');
/*!40000 ALTER TABLE `luchthaven` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maatschappij`
--

DROP TABLE IF EXISTS `maatschappij`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maatschappij` (
  `maatschappij_id` int unsigned NOT NULL AUTO_INCREMENT,
  `naam` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`maatschappij_id`),
  UNIQUE KEY `maatschappij_id_UNIQUE` (`maatschappij_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maatschappij`
--

LOCK TABLES `maatschappij` WRITE;
/*!40000 ALTER TABLE `maatschappij` DISABLE KEYS */;
INSERT INTO `maatschappij` VALUES (2,'KLM');
/*!40000 ALTER TABLE `maatschappij` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tijdgebaseerde_data`
--

DROP TABLE IF EXISTS `tijdgebaseerde_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tijdgebaseerde_data` (
  `vlucht_id` int unsigned NOT NULL,
  `opgehaald_tijdstip` timestamp NOT NULL,
  `prijs` float NOT NULL,
  `vrije_plaatsen` int NOT NULL,
  PRIMARY KEY (`vlucht_id`,`opgehaald_tijdstip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tijdgebaseerde_data`
--

LOCK TABLES `tijdgebaseerde_data` WRITE;
/*!40000 ALTER TABLE `tijdgebaseerde_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `tijdgebaseerde_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vlucht`
--

DROP TABLE IF EXISTS `vlucht`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vlucht` (
  `vlucht_id` int unsigned NOT NULL AUTO_INCREMENT,
  `flightkey` varchar(255) DEFAULT NULL,
  `vluchtnummer` varchar(40) DEFAULT NULL,
  `vertrek_tijdstip` timestamp NOT NULL,
  `aankomst_tijdstip` timestamp NOT NULL,
  `aantal_stops` int unsigned DEFAULT NULL,
  `maatschappij_id` int unsigned DEFAULT NULL,
  `aankomst_luchthaven` int unsigned DEFAULT NULL,
  `vertrek_luchthaven` int unsigned DEFAULT NULL,
  PRIMARY KEY (`vlucht_id`),
  UNIQUE KEY `vlucht_id_UNIQUE` (`vlucht_id`),
  UNIQUE KEY `flightkey_UNIQUE` (`flightkey`),
  KEY `vlucht_luchthaven_idx` (`vertrek_luchthaven`),
  KEY `aankomst_luchthaven_idx` (`aankomst_luchthaven`),
  KEY `maatschappij_idx` (`maatschappij_id`),
  CONSTRAINT `aankomst_luchthaven` FOREIGN KEY (`aankomst_luchthaven`) REFERENCES `luchthaven` (`luchthaven_id`),
  CONSTRAINT `maatschappij` FOREIGN KEY (`maatschappij_id`) REFERENCES `maatschappij` (`maatschappij_id`),
  CONSTRAINT `vertrek_luchthaven` FOREIGN KEY (`vertrek_luchthaven`) REFERENCES `luchthaven` (`luchthaven_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vlucht`
--

LOCK TABLES `vlucht` WRITE;
/*!40000 ALTER TABLE `vlucht` DISABLE KEYS */;
/*!40000 ALTER TABLE `vlucht` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'dep_database'
--
/*!50003 DROP PROCEDURE IF EXISTS `insert_record` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_record`(
    IN `maatschappij_naam` VARCHAR(255),
    IN `vertrek_airport_code` VARCHAR(255),
    IN `vertrek_luchthaven_naam` VARCHAR(255),
    IN `aankomst_airport_code` VARCHAR(255),
    IN `aankomst_luchthaven_naam` VARCHAR(255),
    IN `opgehaald_tijdstip` TIMESTAMP,
    IN `prijs` FLOAT,
    IN `vrije_plaatsen` INT,
    IN `flightkey` VARCHAR(255),
    IN `vluchtnummer` VARCHAR(255),
    IN `aankomst_tijdstip` TIMESTAMP,
    IN `vertrek_tijdstip` TIMESTAMP,
    IN `aantal_stops` INT
)
BEGIN

	
	
    
    IF NOT EXISTS (SELECT * FROM maatschappij WHERE maatschappij.naam = maatschappij_naam LIMIT 1) THEN
        INSERT INTO maatschappij (naam) VALUES (maatschappij_naam);
    END IF;
    SELECT maatschappij_id INTO @maatschappij_id FROM maatschappij WHERE maatschappij.naam = maatschappij_naam LIMIT 1;
    
    
    
    IF NOT EXISTS (SELECT * FROM luchthaven WHERE luchthaven.airport_code = vertrek_airport_code LIMIT 1) THEN 
        INSERT INTO luchthaven (airport_code, naam) VALUES (vertrek_airport_code, vertrek_luchthaven_naam);
    END IF;
    SELECT luchthaven_id INTO @vertrek_luchthaven_id FROM luchthaven WHERE luchthaven.airport_code = vertrek_airport_code LIMIT 1;

    
    IF NOT EXISTS (SELECT * FROM luchthaven WHERE luchthaven.airport_code = aankomst_airport_code LIMIT 1) THEN 
        INSERT INTO luchthaven (airport_code, naam) VALUES (aankomst_airport_code, aankomst_luchthaven_naam);
    END IF;
    SELECT luchthaven_id INTO @aankomst_luchthaven_id FROM luchthaven WHERE luchthaven.airport_code = aankomst_airport_code LIMIT 1;

    
    IF NOT EXISTS (SELECT * FROM vlucht WHERE vlucht.flightkey = flightkey LIMIT 1) THEN
        INSERT INTO vlucht 
            (flightkey, 
            vluchtnummer, 
            vertrek_tijdstip, 
            aankomst_tijdstip, 
            aantal_stops, 
            maatschappij_id, 
            aankomst_luchthaven, 
            vertrek_luchthaven) 
        VALUES 
            (flightkey,
            vluchtnummer,
            vertrek_tijdstip,
            aankomst_tijdstip,
            aantal_stops,
            maatschappij_id,
            @aankomst_luchthaven_id,
            @vertrek_luchthaven_id);
            
    END IF;
    
    
    SELECT vlucht_id INTO @flight_id FROM vlucht WHERE vlucht.flightkey = flightkey LIMIT 1;

    
    INSERT INTO tijdgebaseerde_data 
        (vlucht_id,
        opgehaald_tijdstip,
        prijs,
        vrije_plaatsen)
    VALUES
        (@flight_id,
        opgehaald_tijdstip,
        prijs,
        vrije_plaatsen);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-26 13:29:20
