-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: contra.cjrbdmxkv84s.ap-south-1.rds.amazonaws.com    Database: homies
-- ------------------------------------------------------
-- Server version	8.0.20

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `booking_mst`
--

DROP TABLE IF EXISTS `booking_mst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking_mst` (
  `BID` int NOT NULL AUTO_INCREMENT,
  `PGID` int NOT NULL,
  `RID` int NOT NULL,
  `UID` int NOT NULL,
  `book_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(20) NOT NULL DEFAULT 'Deactivated' COMMENT 'booked/canceled',
  `amount` int DEFAULT NULL COMMENT 'it will be retrieved from token amount from room_mst table',
  PRIMARY KEY (`BID`),
  KEY `ROOM_TO_BID_idx` (`RID`),
  KEY `USER_TO_BOOK_idx` (`UID`),
  KEY `PGID_idx` (`PGID`),
  CONSTRAINT `PGID` FOREIGN KEY (`PGID`) REFERENCES `pg_mst` (`PGID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ROOM_TO_BOOK` FOREIGN KEY (`RID`) REFERENCES `room_mst` (`RID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `USER_TO_BOOK` FOREIGN KEY (`UID`) REFERENCES `user_mst` (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking_mst`
--

LOCK TABLES `booking_mst` WRITE;
/*!40000 ALTER TABLE `booking_mst` DISABLE KEYS */;
INSERT INTO `booking_mst` VALUES (14,8,2,2,'2021-02-05 07:10:29','Activated',2700),(17,8,1,2,'2021-02-14 15:47:59','Declined',300),(21,12,13,2,'2021-02-16 11:52:31','Declined',100),(22,12,13,2,'2021-02-16 11:53:07','Deactivated',100);
/*!40000 ALTER TABLE `booking_mst` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facility_mst`
--

DROP TABLE IF EXISTS `facility_mst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facility_mst` (
  `FID` int NOT NULL AUTO_INCREMENT,
  `PGID` int NOT NULL,
  `amenity` varchar(70) DEFAULT NULL,
  `amenity_type` varchar(10) DEFAULT NULL COMMENT 'amenity_type means COMMOM / SPECIAL amenity',
  PRIMARY KEY (`FID`),
  KEY `PGID_idx` (`PGID`),
  CONSTRAINT `PG_TO_FACILITY` FOREIGN KEY (`PGID`) REFERENCES `pg_mst` (`PGID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=175 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facility_mst`
--

LOCK TABLES `facility_mst` WRITE;
/*!40000 ALTER TABLE `facility_mst` DISABLE KEYS */;
INSERT INTO `facility_mst` VALUES (120,16,'AC','common'),(121,16,'Laundry','common'),(122,16,'Cooking','common'),(125,15,'Cooking','common'),(126,15,'Parking','common'),(128,17,'Parking','common'),(129,17,'Cooking','common'),(132,18,'Cooking','common'),(133,18,'Guests','common'),(134,18,'Parking','common'),(150,8,'AC','common'),(151,8,'Cooking','common'),(152,8,'Parking','common'),(164,10,'Cooking ','common'),(165,10,'Food','common'),(172,12,'Cooking','common'),(173,12,'Laundry','common'),(174,12,'AC','common');
/*!40000 ALTER TABLE `facility_mst` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `FID` int NOT NULL AUTO_INCREMENT,
  `PGID` int NOT NULL,
  `UID` int NOT NULL,
  `feed_date` timestamp NULL DEFAULT NULL,
  `feed_text` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`FID`),
  KEY `PGID_TO_FEEDBACK_idx` (`PGID`),
  KEY `USER_TO_FEEDBACK_idx` (`UID`),
  CONSTRAINT `PGID_TO_FEEDBACK` FOREIGN KEY (`PGID`) REFERENCES `pg_mst` (`PGID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `USER_TO_FEEDBACK` FOREIGN KEY (`UID`) REFERENCES `user_mst` (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (3,8,2,'2020-11-05 00:00:00','It was a good experience staying. It was affordable and the management family has very good manners and very homely. I loved the dog there he was very friendly. Met a french guy and had a nice convers'),(4,8,2,'2021-02-11 00:00:00','One of the best PG in Ahmedabad.');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image_mst`
--

DROP TABLE IF EXISTS `image_mst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image_mst` (
  `IMID` int NOT NULL AUTO_INCREMENT,
  `PGID` int NOT NULL,
  `RID` int NOT NULL,
  `file_path` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`IMID`),
  KEY `RID_idx` (`RID`),
  KEY `PG_TO_IMAGE_idx` (`PGID`),
  CONSTRAINT `PG_TO_IMAGE` FOREIGN KEY (`PGID`) REFERENCES `pg_mst` (`PGID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ROOM_TO_IMAGE` FOREIGN KEY (`RID`) REFERENCES `room_mst` (`RID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_mst`
--

LOCK TABLES `image_mst` WRITE;
/*!40000 ALTER TABLE `image_mst` DISABLE KEYS */;
/*!40000 ALTER TABLE `image_mst` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pg_mst`
--

DROP TABLE IF EXISTS `pg_mst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pg_mst` (
  `PGID` int NOT NULL AUTO_INCREMENT,
  `UID` int NOT NULL,
  `pg_name` varchar(45) DEFAULT NULL,
  `pg_gender` varchar(7) DEFAULT NULL,
  `addr_1` varchar(45) DEFAULT NULL,
  `addr_2` varchar(45) DEFAULT NULL,
  `area` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `state` varchar(45) DEFAULT NULL,
  `pincode` int DEFAULT NULL,
  `total_rooms` int DEFAULT NULL,
  `latitude` varchar(45) DEFAULT NULL,
  `longitude` varchar(45) DEFAULT NULL,
  `map` varchar(512) DEFAULT NULL,
  `prop_desc` varchar(200) DEFAULT NULL,
  `image_1` varchar(100) DEFAULT NULL,
  `image_2` varchar(100) DEFAULT NULL,
  `image_3` varchar(100) DEFAULT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'Activated',
  `hidden` varchar(10) NOT NULL DEFAULT 'no',
  PRIMARY KEY (`PGID`),
  KEY `pg_userMst_idx` (`UID`),
  CONSTRAINT `pg_userMst` FOREIGN KEY (`UID`) REFERENCES `user_mst` (`UID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pg_mst`
--

LOCK TABLES `pg_mst` WRITE;
/*!40000 ALTER TABLE `pg_mst` DISABLE KEYS */;
INSERT INTO `pg_mst` VALUES (8,1,'Royal Paying Guest','Boys','F101 Akash apartment','Near Municipal Market','Navrangpura','Ahmedabad City','Gujarat',380009,4,NULL,NULL,'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d8732.843996920034!2d72.55671706270509!3d23.034468982634696!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x3c0263ae214ee429!2sRoyal%20PG!5e0!3m2!1sen!2sin!4v1612857066491!5m2!1sen!2sin','Located in a safe neighborhood this all men PG offers various modern amenities for your comfort such as TV AC Food Wi-Fi etc.This PG is nearby major commercial and educational hubs.',NULL,NULL,NULL,'Activated','no'),(10,4,'Antara Paying Guest','Girls','G206 Manik society','Near Agam Tower','Bodakdev','Ahmedabad City','Gujarat',380054,3,NULL,NULL,'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d5192.515497581997!2d72.52051687286897!3d23.03614564999849!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x65d4a8508a03fbcc!2sANTARA%20PAYING%20GUEST%20ACCOMODATION!5e0!3m2!1sen!2sin!4v1612857174840!5m2!1sen!2sin','It is a Paying Guest and is open for rent. It is very spacious and gets ample light and cross ventilation. Available at a very competitive price','parikh.madhav1999@gmail.com_WhatsApp_Image_2020-12-19_at_00.24.39.jpeg','parikh.madhav1999@gmail.com_WhatsApp_Image_2020-12-19_at_00.24.39.jpeg','parikh.madhav1999@gmail.com_WhatsApp_Image_2020-12-19_at_00.24.39.jpeg','Activated','no'),(12,1,'Swarg Paying Guest Services','Boys','f-101 surel appartments','Near Mochcha cafe','thaltej','Ahmedabad City','Gujarat',380066,5,NULL,NULL,'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d117466.81761865909!2d72.53913841447023!3d23.06639821140428!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x395e848b59469a73%3A0x9171ed352848e4f!2sParadise%20Pg!5e0!3m2!1sen!2sin!4v1613470517819!5m2!1sen!2sin','Its a good pg',NULL,NULL,NULL,'Activated','no'),(15,12,'Kanha PG','Girls','307, devashish business park','nr leapord circle, above mocha cafe, ','Bodakdev','Ahmedabad City','Gujarat',380054,4,NULL,NULL,'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3522.3321855926174!2d78.2543438150688!3d28.01432118266584!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3974a4cec01d278b%3A0x33cfd37cf01d4565!2sKanha%20Paying%20Guest%20Hostel!5e0!3m2!1sen!2sin!4v1613470460451!5m2!1sen!2sin',NULL,NULL,NULL,NULL,'Activated','no'),(16,13,'VV Paying Guests','Girls','4 Ratnaakar Halycon','Jodhpur Gam Rd','Jodhpur Village','Ahmedabad City','Gujarat',380054,4,NULL,NULL,'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d8733.301575793714!2d72.50427929605661!3d23.027407141830317!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x395e9b2c36ac5871%3A0xd1e5ed475760242e!2sRatnaakar%20Halcyon!5e0!3m2!1sen!2sin!4v1613468409365!5m2!1sen!2sin',NULL,NULL,NULL,NULL,'Activated','no'),(17,14,'Surya Paying Guest','Boys','23, RACHANA NAKSHATRA','AT HAZARIPAHAD,','college street','Nagpur','Gujarat',380054,4,NULL,NULL,'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3720.397770065033!2d79.03258301493514!3d21.17635188591857!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bd4c14823f1d233%3A0xda4aeb1afd66b9d3!2sRACHANA%20NAKSHATRA%20ASHWINI!5e0!3m2!1sen!2sin!4v1613468948080!5m2!1sen!2sin',NULL,NULL,NULL,NULL,'Activated','no'),(18,15,'Rachana PG','Boys','45-C rafel city','near panipura','bhatol','Rajkot','Gujarat',459980,3,NULL,NULL,'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d58752.68013087644!2d72.54702056919348!3d23.02221139394784!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x395e84f53fffffff%3A0x3a1b57cc6b2f5cb5!2sRachana%20Infrastrructure!5e0!3m2!1sen!2sin!4v1613471331172!5m2!1sen!2sin','it\'s also a good PG',NULL,NULL,NULL,'Activated','no');
/*!40000 ALTER TABLE `pg_mst` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room_mst`
--

DROP TABLE IF EXISTS `room_mst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room_mst` (
  `RID` int NOT NULL AUTO_INCREMENT,
  `PGID` int NOT NULL,
  `total_beds` int DEFAULT NULL,
  `avail_beds` int DEFAULT NULL,
  `AC` varchar(4) DEFAULT NULL,
  `TV` varchar(4) DEFAULT NULL,
  `rent` int DEFAULT NULL,
  `token_amt` int DEFAULT NULL COMMENT 'it will be calculated as 1/3rd of room rent and will be automatically filled (through calculations.',
  `rhidden` varchar(10) NOT NULL DEFAULT 'no',
  PRIMARY KEY (`RID`),
  KEY `PGID_idx` (`PGID`),
  CONSTRAINT `PGID_TO_ROOM` FOREIGN KEY (`PGID`) REFERENCES `pg_mst` (`PGID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room_mst`
--

LOCK TABLES `room_mst` WRITE;
/*!40000 ALTER TABLE `room_mst` DISABLE KEYS */;
INSERT INTO `room_mst` VALUES (1,8,3,2,'1','1',9500,300,'no'),(2,8,3,2,'1','0',10000,270,'no'),(5,8,5,4,'1','0',10000,250,'no'),(7,8,4,3,'1','1',9500,250,'no'),(9,10,3,2,'0','0',6500,500,'no'),(10,10,5,4,'1','1',10000,200,'no'),(12,10,4,1,'0','1',5000,100,'no'),(13,12,5,5,'1','1',3000,100,'no'),(14,12,2,2,'0','1',6500,170,'no'),(15,12,3,2,'1','1',2000,500,'no'),(16,12,5,4,'0','0',1000,200,'no'),(17,12,4,1,'1','0',4000,150,'no'),(18,15,2,2,'1','1',1000,250,'no'),(19,15,5,4,'0','0',2300,250,'no'),(20,15,4,2,'1','0',1800,250,'no'),(21,15,5,4,'0','1',1700,150,'no'),(22,16,4,4,'1','1',2700,300,'no'),(23,16,3,1,'1','1',2000,100,'no'),(24,16,2,1,'0','0',1200,100,'no'),(25,16,4,2,'1','0',1500,170,'no'),(26,17,5,4,'0','1',1500,120,'no'),(27,17,4,2,'1','1',2000,130,'no'),(28,17,4,1,'0','1',2500,170,'no'),(29,17,4,2,'0','0',3000,300,'no'),(30,18,5,3,'1','1',3500,250,'no'),(31,18,2,1,'1','1',3200,320,'no'),(34,18,3,3,'1','0',4000,250,'no');
/*!40000 ALTER TABLE `room_mst` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_mst`
--

DROP TABLE IF EXISTS `transaction_mst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_mst` (
  `tid` varchar(30) NOT NULL,
  `date` date NOT NULL,
  `tstatus` varchar(10) NOT NULL,
  `bid` int DEFAULT NULL,
  PRIMARY KEY (`tid`),
  KEY `bid` (`bid`),
  CONSTRAINT `transaction_mst_ibfk_4` FOREIGN KEY (`bid`) REFERENCES `booking_mst` (`BID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_mst`
--

LOCK TABLES `transaction_mst` WRITE;
/*!40000 ALTER TABLE `transaction_mst` DISABLE KEYS */;
INSERT INTO `transaction_mst` VALUES ('eHX09bXC','2021-02-16','success',14),('KXtOwPTY','2021-02-16','success',14);
/*!40000 ALTER TABLE `transaction_mst` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_mst`
--

DROP TABLE IF EXISTS `user_mst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_mst` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `UTMID` int NOT NULL,
  `fname` varchar(45) DEFAULT NULL,
  `mname` varchar(45) DEFAULT NULL,
  `lname` varchar(45) DEFAULT NULL,
  `email` varchar(45) NOT NULL,
  `phone` varchar(13) NOT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(7) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `addr1` varchar(45) DEFAULT NULL,
  `addr2` varchar(45) DEFAULT NULL,
  `area` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `state` varchar(45) DEFAULT NULL,
  `pincode` int DEFAULT NULL,
  `country` varchar(60) DEFAULT NULL,
  `authorised` varchar(12) DEFAULT 'Activated',
  `id_method` varchar(45) DEFAULT NULL COMMENT 'aadhar/pan card/driving license/voter id card',
  `id_proof` varchar(45) DEFAULT NULL,
  `id_photo` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`UID`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `phone_UNIQUE` (`phone`),
  KEY `UTM_TO_USER_idx` (`UTMID`),
  CONSTRAINT `UTM_TO_USER` FOREIGN KEY (`UTMID`) REFERENCES `user_type_mst` (`UTMID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_mst`
--

LOCK TABLES `user_mst` WRITE;
/*!40000 ALTER TABLE `user_mst` DISABLE KEYS */;
INSERT INTO `user_mst` VALUES (1,2,'Madhav','Nita','Parikh','parikh.madhav1999@gmail.com','9998256749','1999-11-03','Male','MParikh','F101 Surel apartment','Nr mocha cafe ','Navrangpura','Ahmedabad City','Gujarat',380054,'India','Activated','PAN','evqpk2130p',NULL),(2,3,'Trilok',NULL,'Sharma','strilok4031@gmail.com','9998747456','1999-12-15','Male','TSharma','B-506 Omkar nagar','B/h ONGC Park','tarsali','Ahmedabad','Gujarat',380056,'India','Activated',NULL,'qewx1245p',NULL),(4,2,'raj','kewal','shah','rajshah65@gmail.com','7845210036','1970-04-17','Male','RShah','f-12, manik society','near petrol pump','thaltej','Ahmedabad','Gujarat',380036,'India','Activated','PAN','yuht6789o',NULL),(5,3,'Nishant ',' ','Jain','nishant.nj4@gmail.com','9521681348','2000-02-27','Male','NJain','C-103, Mahavir Apartment','Street no. 6 ','New Colony','Dungarpur','Rajasthan',314001,'India','Activated','PAN','bdqre9430j',NULL),(7,2,'Bhupender ',NULL,'Kumar','bhupenderkumarcr7@gmail.com','9456486452','1999-08-12','Male','BKumar','D-232, Pragati Society','Nr. Petrol Pump','Railway Colony','Jhansi','Uttar Pradesh',284127,'India','Activated','PAN ','fhshf3424f',NULL),(10,1,'Hitarth','Ajay','Parikh','hitarth.parikh@gmail.com','9997858997','1999-03-18','Male','HParikh','A203,Tirthdham Tenament','Street no. 6 ','Bodakdev','Ahmedabad','Gujarat',380054,'India','Activated','PAN','qwae2343q',NULL),(12,2,'Alok',NULL,'Sharma','aloks2282@gmail.com','9664817006','1997-08-22','male','ASharma','a506,omkar moti1 ','nr kamla park','tarsali','vadodara','Gujarat',390009,'India','Activated','PAN','kglls2312h',NULL),(13,2,'Miloni',NULL,'Shah','shahmiloni10@gmail.com','9426490276','1999-04-21','Female','MShah','S-132 Prakruti Row Houses','Street no. 6 ','shivnagar','Himatnagar','Gujarat',380054,'India','Activated','PAN','qaae2343q',NULL),(14,2,'Deeksha',NULL,'Sharma','deeksha@gmail.com','9998898786','1996-03-11','Female','DSharma','708,aatma heights','ajwapal road','bopal','Rajkot','Gujarat',450009,'India','Activated','PAN','aksle3345a',NULL),(15,2,'Ajay ','maman','Shekhwat','ajay123@gmail.com','7778989087','1992-09-22','Male','AShekh','33-d,nand resedency','pani tanki road','bansalpur','Surat','Gujarat',340033,'India','Activated','PAN','khgls2232g',NULL),(16,3,'jay','kumar','shesha','jayshesha@gmail.com','7845623659','1999-03-12','Female','JShesha','f-89, shanti nagar','Nr.game ground','sadar bazar','kanpur','Uttar Pradesh',284563,'India','Activated','PAN','qweas1244p',NULL);
/*!40000 ALTER TABLE `user_mst` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_type_mst`
--

DROP TABLE IF EXISTS `user_type_mst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_type_mst` (
  `UTMID` int NOT NULL AUTO_INCREMENT,
  `role` varchar(45) NOT NULL,
  PRIMARY KEY (`UTMID`),
  UNIQUE KEY `role_UNIQUE` (`role`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_type_mst`
--

LOCK TABLES `user_type_mst` WRITE;
/*!40000 ALTER TABLE `user_type_mst` DISABLE KEYS */;
INSERT INTO `user_type_mst` VALUES (1,'Admin'),(2,'Owner'),(3,'User');
/*!40000 ALTER TABLE `user_type_mst` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlist`
--

DROP TABLE IF EXISTS `wishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wishlist` (
  `WID` int NOT NULL AUTO_INCREMENT,
  `PGID` int NOT NULL,
  `UID` int NOT NULL,
  PRIMARY KEY (`WID`),
  KEY `PG_TO_WISH_idx` (`PGID`),
  KEY `USER_TO_WISH_idx` (`UID`),
  CONSTRAINT `PG_TO_WISH` FOREIGN KEY (`PGID`) REFERENCES `pg_mst` (`PGID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `USER_TO_WISH` FOREIGN KEY (`UID`) REFERENCES `user_mst` (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlist`
--

LOCK TABLES `wishlist` WRITE;
/*!40000 ALTER TABLE `wishlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `wishlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'homies'
--
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-02-16 18:09:47
