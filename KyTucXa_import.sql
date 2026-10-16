-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: mysql-361c2bb2-patrolislove-4617.f.aivencloud.com    Database: KyTucXa
-- ------------------------------------------------------
-- Server version	8.4.8

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
-- Current Database: `KyTucXa`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `KyTucXa` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `KyTucXa`;

--
-- Table structure for table `DANG_KY_XE_THANG`
--

DROP TABLE IF EXISTS `DANG_KY_XE_THANG`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DANG_KY_XE_THANG` (
  `MaDangKy` int NOT NULL AUTO_INCREMENT,
  `DonGiaThang` int NOT NULL DEFAULT '100000',
  `NgayBatDau` date NOT NULL DEFAULT (curdate()),
  `NgayKetThuc` date NOT NULL,
  `MaXe` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `MaSV` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`MaDangKy`),
  KEY `fk_DK_XE` (`MaXe`),
  KEY `fk_DK_SV` (`MaSV`),
  CONSTRAINT `fk_DK_SV` FOREIGN KEY (`MaSV`) REFERENCES `SINHVIEN` (`MaSV`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_DK_XE` FOREIGN KEY (`MaXe`) REFERENCES `XE` (`MaXe`) ON UPDATE RESTRICT,
  CONSTRAINT `chk_dkxe_gia` CHECK ((`DonGiaThang` > 0)),
  CONSTRAINT `chk_ngay_ket_thuc` CHECK ((`NgayKetThuc` >= `NgayBatDau`))
) ENGINE=InnoDB AUTO_INCREMENT=30012 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DANG_KY_XE_THANG`
--

LOCK TABLES `DANG_KY_XE_THANG` WRITE;
/*!40000 ALTER TABLE `DANG_KY_XE_THANG` DISABLE KEYS */;
INSERT INTO `DANG_KY_XE_THANG` VALUES (30001,100000,'2026-10-01','2026-10-31','XE00001','SV00001'),(30002,100000,'2026-10-01','2026-10-31','XE00002','SV00001'),(30003,100000,'2026-10-01','2026-10-31','XE00003','SV00002'),(30004,100000,'2026-10-01','2026-10-31','XE00004','SV00003'),(30005,100000,'2026-10-01','2026-10-31','XE00005','SV00004'),(30006,100000,'2026-10-01','2026-10-31','XE00006','SV00005'),(30007,100000,'2026-10-01','2026-10-31','XE00007','SV00006'),(30008,100000,'2026-10-01','2026-10-31','XE00008','SV00002'),(30009,100000,'2026-10-01','2026-10-31','XE00009','SV00007'),(30010,100000,'2026-10-01','2026-10-31','XE00010','SV00008'),(30011,100000,'2026-10-01','2026-10-31','XE00011','SV00009');
/*!40000 ALTER TABLE `DANG_KY_XE_THANG` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'REAL_AS_FLOAT,PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,ONLY_FULL_GROUP_BY,ANSI,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`avnadmin`@`%`*/ /*!50003 TRIGGER `trg_dk_xe_toi_da_2_bi` BEFORE INSERT ON `DANG_KY_XE_THANG` FOR EACH ROW BEGIN
    DECLARE so_dang_ky_chua_het_han INT DEFAULT 0;

    IF NEW.MaSV IS NULL OR NEW.NgayBatDau IS NULL OR NEW.NgayKetThuc IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'MaSV, NgayBatDau va NgayKetThuc khong duoc de trong';
    END IF;

    IF NEW.NgayKetThuc < NEW.NgayBatDau THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'NgayKetThuc khong duoc truoc NgayBatDau';
    END IF;

    SELECT COUNT(*)
      INTO so_dang_ky_chua_het_han
      FROM DANG_KY_XE_THANG
     WHERE MaSV = NEW.MaSV
       AND NgayKetThuc >= CURDATE();

    IF so_dang_ky_chua_het_han >= 2
       AND NEW.NgayKetThuc >= CURDATE() THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Moi sinh vien chi duoc co toi da 2 dang ky xe thang chua het han';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'REAL_AS_FLOAT,PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,ONLY_FULL_GROUP_BY,ANSI,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`avnadmin`@`%`*/ /*!50003 TRIGGER `trg_dk_xe_toi_da_2_bu` BEFORE UPDATE ON `DANG_KY_XE_THANG` FOR EACH ROW BEGIN
    DECLARE so_dang_ky_chua_het_han INT DEFAULT 0;

    IF NEW.MaSV IS NULL OR NEW.NgayBatDau IS NULL OR NEW.NgayKetThuc IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'MaSV, NgayBatDau va NgayKetThuc khong duoc de trong';
    END IF;

    IF NEW.NgayKetThuc < NEW.NgayBatDau THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'NgayKetThuc khong duoc truoc NgayBatDau';
    END IF;

    SELECT COUNT(*)
      INTO so_dang_ky_chua_het_han
      FROM DANG_KY_XE_THANG
     WHERE MaSV = NEW.MaSV
       AND NgayKetThuc >= CURDATE()
       AND MaDangKy <> OLD.MaDangKy;

    IF so_dang_ky_chua_het_han >= 2
       AND NEW.NgayKetThuc >= CURDATE() THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Moi sinh vien chi duoc co toi da 2 dang ky xe thang chua het han';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `DICHVU`
--

DROP TABLE IF EXISTS `DICHVU`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DICHVU` (
  `MaDV` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `TenDV` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `DonGia` int NOT NULL,
  `ThoiGianSuDungTheoNgay` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`MaDV`),
  CONSTRAINT `chk_dichvu_gia_duong` CHECK ((`DonGia` > 0)),
  CONSTRAINT `chk_dichvu_thoigian_duong` CHECK ((`ThoiGianSuDungTheoNgay` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DICHVU`
--

LOCK TABLES `DICHVU` WRITE;
/*!40000 ALTER TABLE `DICHVU` DISABLE KEYS */;
INSERT INTO `DICHVU` VALUES ('DV00001','Giat la',25000,1),('DV00002','Trong xe ve thang',100000,30),('DV00003','Cho thue xe',50000,1),('DV00004','An uong',35000,1);
/*!40000 ALTER TABLE `DICHVU` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HOADON`
--

DROP TABLE IF EXISTS `HOADON`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `HOADON` (
  `MaHoaDon` int NOT NULL AUTO_INCREMENT,
  `NgayLap` date NOT NULL DEFAULT (curdate()),
  `TongTien` bigint NOT NULL,
  `MaSV` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`MaHoaDon`),
  KEY `fk_HOADON_SV` (`MaSV`),
  CONSTRAINT `fk_HOADON_SV` FOREIGN KEY (`MaSV`) REFERENCES `SINHVIEN` (`MaSV`) ON UPDATE RESTRICT,
  CONSTRAINT `chk_hoadon_tong_khong_am` CHECK ((`TongTien` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HOADON`
--

LOCK TABLES `HOADON` WRITE;
/*!40000 ALTER TABLE `HOADON` DISABLE KEYS */;
INSERT INTO `HOADON` VALUES (1,'2026-10-10',958000,'SV00001'),(2,'2026-10-10',875000,'SV00002'),(3,'2026-10-10',720000,'SV00003'),(4,'2026-10-10',745000,'SV00004'),(5,'2026-10-10',1140000,'SV00005'),(6,'2026-10-10',1025000,'SV00006'),(7,'2026-10-14',1385000,'SV00007'),(8,'2026-10-14',2090000,'SV00008'),(9,'2026-10-14',1085000,'SV00009'),(10,'2026-10-14',1035000,'SV00010');
/*!40000 ALTER TABLE `HOADON` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `KHACH`
--

DROP TABLE IF EXISTS `KHACH`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `KHACH` (
  `K_CCCD` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `HoTen` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `NgaySinh` date DEFAULT NULL,
  PRIMARY KEY (`K_CCCD`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `KHACH`
--

LOCK TABLES `KHACH` WRITE;
/*!40000 ALTER TABLE `KHACH` DISABLE KEYS */;
INSERT INTO `KHACH` VALUES ('TEST-KH-0001','Nguyen Minh Anh','2002-05-17'),('TEST-KH-0002','Tran Quoc Bao','2001-12-09'),('TEST-KH-0003','Le Thu Ha','2003-03-21'),('TEST-KH-0004','Pham Gia Huy','2002-08-16'),('TEST-KH-0005','Vo Thanh Long','2002-10-11'),('TEST-KH-0006','Bui Ngoc Mai','2003-07-24'),('TEST-KH-0007','Dang Tuan Kiet','2001-02-13'),('TEST-KH-0008','Hoang Thu Trang','2002-04-27');
/*!40000 ALTER TABLE `KHACH` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LUOT_XE`
--

DROP TABLE IF EXISTS `LUOT_XE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LUOT_XE` (
  `MaLuotXe` int NOT NULL AUTO_INCREMENT,
  `ThoiGianGui` datetime NOT NULL,
  `ThoiGianLay` datetime DEFAULT NULL,
  `SoTienPhatSinh` int NOT NULL,
  `MaXe` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`MaLuotXe`),
  KEY `fk_LUOTXE_XE` (`MaXe`),
  CONSTRAINT `fk_LUOTXE_XE` FOREIGN KEY (`MaXe`) REFERENCES `XE` (`MaXe`),
  CONSTRAINT `chk_luotxe_thoigian_hople` CHECK (((`ThoiGianGui` is not null) and ((`ThoiGianLay` is null) or (`ThoiGianLay` >= `ThoiGianGui`)))),
  CONSTRAINT `chk_luotxe_tien` CHECK ((`SoTienPhatSinh` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LUOT_XE`
--

LOCK TABLES `LUOT_XE` WRITE;
/*!40000 ALTER TABLE `LUOT_XE` DISABLE KEYS */;
INSERT INTO `LUOT_XE` VALUES (1,'2026-10-05 08:00:00','2026-10-05 12:00:00',0,'XE00001'),(2,'2026-10-05 13:00:00','2026-10-05 16:00:00',0,'XE00001'),(3,'2026-10-05 17:00:00','2026-10-05 19:00:00',3000,'XE00001'),(4,'2026-10-06 08:10:00','2026-10-06 17:30:00',0,'XE00005'),(5,'2026-10-11 08:00:00','2026-10-11 12:00:00',0,'XE00009'),(6,'2026-10-12 08:00:00','2026-10-12 12:00:00',0,'XE00010'),(7,'2026-10-11 07:30:00','2026-10-11 11:30:00',0,'XE00011'),(8,'2026-10-12 07:30:00','2026-10-12 11:30:00',0,'XE00011'),(9,'2026-10-13 07:30:00','2026-10-13 11:30:00',3000,'XE00011'),(10,'2026-10-11 09:00:00','2026-10-11 17:00:00',5000,'XE00012');
/*!40000 ALTER TABLE `LUOT_XE` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'REAL_AS_FLOAT,PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,ONLY_FULL_GROUP_BY,ANSI,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`avnadmin`@`%`*/ /*!50003 TRIGGER `them_luot_xe` BEFORE INSERT ON `LUOT_XE` FOR EACH ROW BEGIN
    declare coDK int;
    declare dem_luot int;
    
    select count(*)
    into coDK
    from DANG_KY_XE_THANG dk
    where date(dk.NgayBatDau) <= curdate() and
			curdate() <= date(dk.NgayKetThuc)
            and new.MaXe = dk.MaXe;
	
    if coDK >= 1 then
        select count(*)
        into dem_luot
        from LUOT_XE lx
        where lx.MaXe = new.MaXe;
        
        if dem_luot >= 2 then
			set new.SoTienPhatSinh = 3000;
		else set new.SoTienPhatSinh = 0;
		end if;
	else set new.SoTienPhatSinh = 3000;
    end if;
    
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `PHONG`
--

DROP TABLE IF EXISTS `PHONG`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PHONG` (
  `SoPhong` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `LoaiPhong` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `DonGiaThang` int NOT NULL,
  `SoNguoiToiDa` int NOT NULL,
  PRIMARY KEY (`SoPhong`),
  CONSTRAINT `chk_phong_gia` CHECK ((`DonGiaThang` > 0)),
  CONSTRAINT `chk_phong_suc_chua` CHECK ((`SoNguoiToiDa` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PHONG`
--

LOCK TABLES `PHONG` WRITE;
/*!40000 ALTER TABLE `PHONG` DISABLE KEYS */;
INSERT INTO `PHONG` VALUES ('101','Thuong',1200000,4),('102','Thuong',1000000,4),('103','Thuong',1100000,4),('201','Chat luong cao',1800000,2),('202','Chat luong cao',1900000,2),('301','Thuong',950000,4);
/*!40000 ALTER TABLE `PHONG` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SINHVIEN`
--

DROP TABLE IF EXISTS `SINHVIEN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SINHVIEN` (
  `MaSV` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `SV_CCCD` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `QueQuan` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `NgaySinh` date DEFAULT NULL,
  `Lop` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `SoPhong` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`MaSV`),
  UNIQUE KEY `SV_CCCD` (`SV_CCCD`),
  KEY `fk_SV_PHONG` (`SoPhong`),
  CONSTRAINT `fk_SV_PHONG` FOREIGN KEY (`SoPhong`) REFERENCES `PHONG` (`SoPhong`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SINHVIEN`
--

LOCK TABLES `SINHVIEN` WRITE;
/*!40000 ALTER TABLE `SINHVIEN` DISABLE KEYS */;
INSERT INTO `SINHVIEN` VALUES ('SV00001','TEST-SV-CCCD-0001','Ha Noi','2004-02-14','CNTT01','101'),('SV00002','TEST-SV-CCCD-0002','Hai Phong','2003-11-03','CNTT01','101'),('SV00003','TEST-SV-CCCD-0003','Da Nang','2004-06-20','HTTT02','102'),('SV00004','TEST-SV-CCCD-0004','Nam Dinh','2003-09-12','HTTT02','102'),('SV00005','TEST-SV-CCCD-0005','Can Tho','2004-01-30','QTKD01','201'),('SV00006','TEST-SV-CCCD-0006','Hue','2003-07-08','QTKD01','201'),('SV00007','TEST-SV-CCCD-0007','Quang Ninh','2004-04-18','CNTT02','103'),('SV00008','TEST-SV-CCCD-0008','Ninh Binh','2003-12-22','HTTT01','202'),('SV00009','TEST-SV-CCCD-0009','Binh Dinh','2004-08-05','QTKD02','301'),('SV00010','TEST-SV-CCCD-0010','Lam Dong','2004-10-02','CNTT02','103');
/*!40000 ALTER TABLE `SINHVIEN` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'REAL_AS_FLOAT,PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,ONLY_FULL_GROUP_BY,ANSI,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`avnadmin`@`%`*/ /*!50003 TRIGGER `SINHVIEN_BEFORE_INSERT` BEFORE INSERT ON `SINHVIEN` FOR EACH ROW BEGIN
  DECLARE v_suc_chua INT;
  DECLARE v_so_sv INT;

  IF NEW.SoPhong IS NOT NULL THEN
    SELECT SoNguoiToiDa INTO v_suc_chua
    FROM PHONG
    WHERE SoPhong = NEW.SoPhong;

    SELECT COUNT(*) INTO v_so_sv
    FROM SINHVIEN
    WHERE SoPhong = NEW.SoPhong;

    IF v_so_sv >= v_suc_chua THEN
      SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Phong da day nguoi';
    END IF;
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'REAL_AS_FLOAT,PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,ONLY_FULL_GROUP_BY,ANSI,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`avnadmin`@`%`*/ /*!50003 TRIGGER `SINHVIEN_BEFORE_UPDATE_PHONG` BEFORE UPDATE ON `SINHVIEN` FOR EACH ROW BEGIN
  DECLARE v_suc_chua INT;
  DECLARE v_so_sv INT;

  IF NEW.SoPhong IS NOT NULL
     AND NOT (NEW.SoPhong <=> OLD.SoPhong) THEN
    SELECT SoNguoiToiDa INTO v_suc_chua
    FROM PHONG
    WHERE SoPhong = NEW.SoPhong;

    SELECT COUNT(*) INTO v_so_sv
    FROM SINHVIEN
    WHERE SoPhong = NEW.SoPhong;

    IF v_so_sv >= v_suc_chua THEN
      SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Phong moi da day nguoi';
    END IF;
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `SUDUNG`
--

DROP TABLE IF EXISTS `SUDUNG`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SUDUNG` (
  `MaSuDung` int NOT NULL AUTO_INCREMENT,
  `NgaySuDung` date NOT NULL DEFAULT (curdate()),
  `SoLuong` int NOT NULL,
  `TongTienDichVu` bigint NOT NULL,
  `MaSV` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `MaDV` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`MaSuDung`),
  KEY `fk_SUDUNG_SV` (`MaSV`),
  KEY `fk_SUDUNG_DV` (`MaDV`),
  CONSTRAINT `fk_SUDUNG_DV` FOREIGN KEY (`MaDV`) REFERENCES `DICHVU` (`MaDV`),
  CONSTRAINT `fk_SUDUNG_SV` FOREIGN KEY (`MaSV`) REFERENCES `SINHVIEN` (`MaSV`),
  CONSTRAINT `chk_sudung_soluong` CHECK ((`SoLuong` > 0)),
  CONSTRAINT `chk_sudung_thongtin_batbuoc` CHECK (((`NgaySuDung` is not null) and (`SoLuong` is not null) and (`TongTienDichVu` is not null))),
  CONSTRAINT `chk_sudung_tongtien` CHECK ((`TongTienDichVu` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SUDUNG`
--

LOCK TABLES `SUDUNG` WRITE;
/*!40000 ALTER TABLE `SUDUNG` DISABLE KEYS */;
INSERT INTO `SUDUNG` VALUES (1,'2026-10-02',2,50000,'SV00001','DV00001'),(2,'2026-10-03',3,105000,'SV00001','DV00004'),(3,'2026-10-04',1,25000,'SV00002','DV00001'),(4,'2026-10-05',1,50000,'SV00003','DV00003'),(5,'2026-10-06',2,70000,'SV00004','DV00004'),(6,'2026-10-07',3,75000,'SV00004','DV00001'),(7,'2026-10-08',4,140000,'SV00005','DV00004'),(8,'2026-10-09',1,25000,'SV00006','DV00001'),(9,'2026-10-10',2,50000,'SV00002','DV00001'),(10,'2026-10-10',2,70000,'SV00003','DV00004'),(11,'2026-10-11',2,50000,'SV00007','DV00001'),(12,'2026-10-12',1,35000,'SV00007','DV00004'),(13,'2026-10-12',2,100000,'SV00008','DV00003'),(14,'2026-10-13',3,105000,'SV00009','DV00004'),(15,'2026-10-13',1,25000,'SV00010','DV00001');
/*!40000 ALTER TABLE `SUDUNG` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'REAL_AS_FLOAT,PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,ONLY_FULL_GROUP_BY,ANSI,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`avnadmin`@`%`*/ /*!50003 TRIGGER `SUDUNG_BEFORE_INSERT` BEFORE INSERT ON `SUDUNG` FOR EACH ROW BEGIN
	declare dongiadv int;
    
    select DonGia
    into dongiadv
    from DICHVU dv
    where new.MaDV = dv.MaDV;
    
    set new.TongTienDichVu = new.SoLuong * dongiadv;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'REAL_AS_FLOAT,PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,ONLY_FULL_GROUP_BY,ANSI,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`avnadmin`@`%`*/ /*!50003 TRIGGER `SUDUNG_BEFORE_UPDATE` BEFORE UPDATE ON `SUDUNG` FOR EACH ROW BEGIN
  DECLARE v_don_gia INT;

  SELECT DonGia INTO v_don_gia
  FROM DICHVU
  WHERE MaDV = NEW.MaDV;

  SET NEW.TongTienDichVu = NEW.SoLuong * v_don_gia;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `THAM`
--

DROP TABLE IF EXISTS `THAM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `THAM` (
  `MaTham` int NOT NULL AUTO_INCREMENT,
  `NgayTham` date NOT NULL DEFAULT (curdate()),
  `MaSV` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `K_CCCD` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`MaTham`),
  KEY `fk_THAM_SV` (`MaSV`),
  KEY `fk_THAM_KHACH` (`K_CCCD`),
  CONSTRAINT `fk_THAM_KHACH` FOREIGN KEY (`K_CCCD`) REFERENCES `KHACH` (`K_CCCD`),
  CONSTRAINT `fk_THAM_SV` FOREIGN KEY (`MaSV`) REFERENCES `SINHVIEN` (`MaSV`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `THAM`
--

LOCK TABLES `THAM` WRITE;
/*!40000 ALTER TABLE `THAM` DISABLE KEYS */;
INSERT INTO `THAM` VALUES (1,'2026-10-03','SV00001','TEST-KH-0001'),(2,'2026-10-05','SV00001','TEST-KH-0001'),(3,'2026-10-06','SV00002','TEST-KH-0002'),(4,'2026-10-08','SV00003','TEST-KH-0001'),(5,'2026-10-09','SV00004','TEST-KH-0003'),(6,'2026-10-10','SV00005','TEST-KH-0002'),(7,'2026-10-09','SV00002','TEST-KH-0004'),(8,'2026-10-10','SV00002','TEST-KH-0001'),(9,'2026-10-11','SV00007','TEST-KH-0005'),(10,'2026-10-12','SV00008','TEST-KH-0006'),(11,'2026-10-13','SV00009','TEST-KH-0007'),(12,'2026-10-14','SV00010','TEST-KH-0008'),(13,'2026-10-14','SV00007','TEST-KH-0006');
/*!40000 ALTER TABLE `THAM` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `XE`
--

DROP TABLE IF EXISTS `XE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `XE` (
  `MaXe` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `BienSo` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `LoaiXe` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MaSV` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`MaXe`),
  UNIQUE KEY `BienSo_UNIQUE` (`BienSo`),
  KEY `fk_XE_SV` (`MaSV`),
  CONSTRAINT `fk_XE_SV` FOREIGN KEY (`MaSV`) REFERENCES `SINHVIEN` (`MaSV`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `XE`
--

LOCK TABLES `XE` WRITE;
/*!40000 ALTER TABLE `XE` DISABLE KEYS */;
INSERT INTO `XE` VALUES ('XE00001','TEST-29A-00001','Xe may','SV00001'),('XE00002','TEST-29A-00002','Xe may','SV00001'),('XE00003','TEST-15A-00003','Xe may','SV00002'),('XE00004','TEST-43A-00004','Xe may','SV00003'),('XE00005','TEST-18A-00005','Xe may','SV00004'),('XE00006','TEST-65A-00006','Xe may','SV00005'),('XE00007','TEST-75A-00007','Xe may','SV00006'),('XE00008','TEST-15A-00008','Xe may','SV00002'),('XE00009','TEST-14A-00009','Xe may','SV00007'),('XE00010','TEST-35A-00010','Xe may','SV00008'),('XE00011','TEST-77A-00011','Xe may','SV00009'),('XE00012','TEST-49A-00012','Xe may','SV00010');
/*!40000 ALTER TABLE `XE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'KyTucXa'
--

--
-- Dumping routines for database 'KyTucXa'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-16  7:33:41
