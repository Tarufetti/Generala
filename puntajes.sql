-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: puntajes
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `jugadores`
--

DROP TABLE IF EXISTS `jugadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jugadores` (
  `ID_JUGADOR` int NOT NULL,
  `NOMBRE_JUGADOR` varchar(20) NOT NULL,
  PRIMARY KEY (`ID_JUGADOR`),
  UNIQUE KEY `NOMBRE_JUGADOR_UNIQUE` (`NOMBRE_JUGADOR`),
  UNIQUE KEY `ID_JUGADOR_UNIQUE` (`ID_JUGADOR`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jugadores`
--

LOCK TABLES `jugadores` WRITE;
/*!40000 ALTER TABLE `jugadores` DISABLE KEYS */;
/*!40000 ALTER TABLE `jugadores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partida`
--

DROP TABLE IF EXISTS `partida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partida` (
  `ID_PARTIDA` int NOT NULL,
  `NOMBRE_PARTIDA` varchar(45) NOT NULL,
  `FECHA` varchar(45) NOT NULL,
  `HORA` varchar(45) NOT NULL,
  PRIMARY KEY (`ID_PARTIDA`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partida`
--

LOCK TABLES `partida` WRITE;
/*!40000 ALTER TABLE `partida` DISABLE KEYS */;
/*!40000 ALTER TABLE `partida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `puntajes`
--

DROP TABLE IF EXISTS `puntajes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `puntajes` (
  `ID_PUNTAJE` int NOT NULL AUTO_INCREMENT,
  `ID_PARTIDA` int NOT NULL,
  `ID_JUGADOR` int NOT NULL,
  `TURNO` int DEFAULT NULL,
  `uno` int DEFAULT NULL,
  `dos` int DEFAULT NULL,
  `tres` int DEFAULT NULL,
  `cuatro` int DEFAULT NULL,
  `cinco` int DEFAULT NULL,
  `seis` int DEFAULT NULL,
  `E` int DEFAULT NULL,
  `F` int DEFAULT NULL,
  `P` int DEFAULT NULL,
  `G` int DEFAULT NULL,
  `GD` int DEFAULT NULL,
  PRIMARY KEY (`ID_PUNTAJE`),
  UNIQUE KEY `ID_PUNTAJE` (`ID_PUNTAJE`),
  KEY `ID_PARTIDA` (`ID_PARTIDA`),
  KEY `ID_JUGADOR` (`ID_JUGADOR`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `puntajes`
--

LOCK TABLES `puntajes` WRITE;
/*!40000 ALTER TABLE `puntajes` DISABLE KEYS */;
/*!40000 ALTER TABLE `puntajes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-24 18:26:35
