-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: autonomo2
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id_cliente` int NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `telefono` int NOT NULL,
  `direccion` varchar(255) NOT NULL,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (10000,'Juan Perez','juan@hotmail.com',987654321,'Quito'),(10001,'Maria Gomez','maria.gomez@gmail.com',912345678,'Guayaquil'),(10002,'Carlos Ruiz','carlos.ruiz@yahoo.com',976543210,'Cuenca'),(10003,'Ana Torres','ana.torres@outlook.com',934567890,'Quito'),(10004,'Luis Fernandez','luisf@gmail.com',998765432,'Loja'),(10005,'Patricia Diaz','patydiaz@gmail.com',956789012,'Ambato'),(10006,'Diego Herrera','diego.h@hotmail.com',923456789,'Manta'),(10007,'Valeria Cedeño','valeria.cedeno@gmail.com',945678901,'Portoviejo'),(10008,'Jorge Zambrano','jorgez@yahoo.com',965432109,'Esmeraldas'),(10009,'Camila Rivas','camila.rivas@gmail.com',912345670,'Riobamba');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_pedido`
--

DROP TABLE IF EXISTS `detalle_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_pedido` (
  `id_detalle` int NOT NULL,
  `cantidad` int NOT NULL,
  `subtotal` float NOT NULL,
  `id_pedido` int DEFAULT NULL,
  `id_pizza` int DEFAULT NULL,
  PRIMARY KEY (`id_detalle`),
  KEY `id_pizza_idx` (`id_pizza`),
  KEY `id_pedido_idx` (`id_pedido`),
  CONSTRAINT `fk_id_pedido` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedidos`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_id_pizza` FOREIGN KEY (`id_pizza`) REFERENCES `pizza` (`id_pizza`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_pedido`
--

LOCK TABLES `detalle_pedido` WRITE;
/*!40000 ALTER TABLE `detalle_pedido` DISABLE KEYS */;
INSERT INTO `detalle_pedido` VALUES (1,2,30,4,7),(2,2,28,1,3),(3,3,25.5,7,10),(4,1,32,9,6),(5,3,27.75,5,2),(6,4,29,3,9),(7,4,31.5,8,1),(8,5,30.25,10,5),(9,5,26.4,6,4),(10,6,33.1,2,8);
/*!40000 ALTER TABLE `detalle_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingrediente_adicional`
--

DROP TABLE IF EXISTS `ingrediente_adicional`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingrediente_adicional` (
  `id_detalle` int DEFAULT NULL,
  `id_ingrediente` int DEFAULT NULL,
  KEY `fk_id_detalle_idx` (`id_detalle`),
  KEY `fk_id_ingrediente_idx` (`id_ingrediente`),
  CONSTRAINT `fk_id_detalle` FOREIGN KEY (`id_detalle`) REFERENCES `detalle_pedido` (`id_detalle`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_id_ingrediente` FOREIGN KEY (`id_ingrediente`) REFERENCES `ingredientes` (`id_ingrediente`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingrediente_adicional`
--

LOCK TABLES `ingrediente_adicional` WRITE;
/*!40000 ALTER TABLE `ingrediente_adicional` DISABLE KEYS */;
INSERT INTO `ingrediente_adicional` VALUES (1,NULL),(2,5),(3,NULL),(4,2),(5,NULL),(6,8),(7,NULL),(8,1),(9,NULL),(10,3);
/*!40000 ALTER TABLE `ingrediente_adicional` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredientes`
--

DROP TABLE IF EXISTS `ingredientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredientes` (
  `id_ingrediente` int NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `precio` float NOT NULL,
  PRIMARY KEY (`id_ingrediente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredientes`
--

LOCK TABLES `ingredientes` WRITE;
/*!40000 ALTER TABLE `ingredientes` DISABLE KEYS */;
INSERT INTO `ingredientes` VALUES (1,'PEPERONI',2),(2,'CHAMPIÑONES',1.5),(3,'JALAPEÑOS',1),(4,'QUESO EXTRA',1.8),(5,'TOCINO',2.2),(6,'POLLO',2.5),(7,'PIÑA',1.3),(8,'ACEITUNAS NEGRAS',1.7),(9,'CARNE MOLIDA',2.4),(10,'CEBOLLA CARAMELIZADA',1.6);
/*!40000 ALTER TABLE `ingredientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metodo_pago`
--

DROP TABLE IF EXISTS `metodo_pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metodo_pago` (
  `id_metodo` int NOT NULL,
  `tipo_pago` varchar(255) NOT NULL,
  PRIMARY KEY (`id_metodo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metodo_pago`
--

LOCK TABLES `metodo_pago` WRITE;
/*!40000 ALTER TABLE `metodo_pago` DISABLE KEYS */;
INSERT INTO `metodo_pago` VALUES (1,'Tarjeta'),(2,'Efectivo'),(3,'Transferencia bancaria'),(4,'PayPal');
/*!40000 ALTER TABLE `metodo_pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `id_pedidos` int NOT NULL,
  `fecha_hora` date NOT NULL,
  `total` float NOT NULL,
  `id_cliente` int DEFAULT NULL,
  `id_metodo` int DEFAULT NULL,
  PRIMARY KEY (`id_pedidos`),
  KEY `fk_id_cliente_idx` (`id_cliente`),
  KEY `fk_id_metodo_idx` (`id_metodo`),
  CONSTRAINT `fk_id_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_id_metodo` FOREIGN KEY (`id_metodo`) REFERENCES `metodo_pago` (`id_metodo`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,'2015-06-13',25,10003,1),(2,'2025-03-16',35.5,10007,3),(3,'2025-03-15',25.75,10001,2),(4,'2025-03-17',50,10008,4),(5,'2025-03-16',42,10005,2),(6,'2025-03-15',30,10000,1),(7,'2025-03-17',45.2,10009,3),(8,'2025-03-16',33.33,10002,4),(9,'2025-03-15',39.99,10004,1),(10,'2025-03-17',47.8,10006,2);
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pizza`
--

DROP TABLE IF EXISTS `pizza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pizza` (
  `id_pizza` int NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripción` varchar(255) NOT NULL,
  `precio_base` float NOT NULL,
  PRIMARY KEY (`id_pizza`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pizza`
--

LOCK TABLES `pizza` WRITE;
/*!40000 ALTER TABLE `pizza` DISABLE KEYS */;
INSERT INTO `pizza` VALUES (1,'Hawayana','Jamón y piña',5),(2,'Pepperoni','Queso mozzarella y pepperoni',6.5),(3,'Cuatro Quesos','Mozzarella, cheddar, azul y parmesano',7),(4,'Vegetariana','Pimiento, champiñones y aceitunas',6),(5,'Mexicana','Chorizo, jalapeños y cebolla',7.5),(6,'Pollo BBQ','Pollo, salsa BBQ y cebolla morada',6.8),(7,'Napolitana','Tomate, ajo y orégano',6),(8,'Margherita','Queso mozzarella y albahaca fresca',5.5),(9,'Carbonara','Tocino, huevo y crema',7.2),(10,'Mar y Tierra','Camarones, carne y queso',8);
/*!40000 ALTER TABLE `pizza` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-27  1:58:42
