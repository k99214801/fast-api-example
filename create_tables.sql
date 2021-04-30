-- MySQL dump 10.13  Distrib 8.0.23, for osx10.16 (x86_64)
--
-- Host: localhost    Database: users
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `sessions`
--

DROP DATABASE IF EXISTS `users`;
CREATE DATABASE `users`;

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions` (
  `row_id` bigint NOT NULL AUTO_INCREMENT COMMENT '테이블 기본 아이디',
  `user_rowid` varchar(255) NOT NULL COMMENT '사용자 테이블 로우 아이디',
  `session_key` varchar(255) NOT NULL COMMENT '세션 키',
  `ip` varchar(20) NOT NULL DEFAULT '0' COMMENT '사용자 아이피',
  `logout` tinyint NOT NULL DEFAULT '0' COMMENT '로그아웃 여부',
  `logout_dt` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '마지막 로그아웃 날짜',
  `created_dt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 날짜(가입 날짜)',
  PRIMARY KEY (`row_id`),
  KEY `idx_session_session_key_logout` (`session_key`,`logout`) USING BTREE,
  KEY `idx_session_user_rowid` (`user_rowid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `row_id` bigint NOT NULL AUTO_INCREMENT COMMENT '테이블 기본 아이디',
  `id` varchar(255) NOT NULL COMMENT '사용자 아이디',
  `password` varchar(255) NOT NULL COMMENT '사용자 비밀번호',
  `leave` tinyint NOT NULL DEFAULT '0' COMMENT '탈퇴 여부',
  `last_login_dt` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '마지막 로그인 날짜',
  `last_logout_dt` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '마지막 로그아웃 날짜',
  `leave_dt` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '탈퇴 날짜',
  `created_dt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 날짜(가입 날짜)',
  PRIMARY KEY (`row_id`),
  KEY `idx_user_id_pw_leave` (`id`,`password`,`leave`) USING BTREE,
  KEY `idx_id_leave` (`id`,`leave`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-30  0:35:27
