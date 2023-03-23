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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'dep_database'
--

--
-- Dumping routines for database 'dep_database'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-23 11:01:14
